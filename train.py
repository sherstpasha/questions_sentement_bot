from torch.utils.data import Sampler
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel, AutoTokenizer, AdamW
from sklearn.model_selection import train_test_split
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.nn.functional as F
import pandas as pd
from torch.optim.lr_scheduler import ReduceLROnPlateau
import argparse


parser = argparse.ArgumentParser(description='Multi-task BERT training script')

parser.add_argument('--epochs', type=int, default=50, help='Number of epochs for training')
parser.add_argument('--lr_start', type=float, default=5e-5, help='Initial learning rate')
parser.add_argument('--train_data_path', type=str, default='train_data_questions_text.csv', help='Path to the training data CSV file')


args = parser.parse_args()

file_path = args.train_data_path 
num_epochs = args.epochs 
lr_start = args.lr_start 


class MultiTaskBERT(nn.Module):
    def __init__(self, model_name, num_classes_list):
        super().__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        self.classifiers = nn.ModuleList([
            nn.Linear(self.bert.config.hidden_size, num_classes) for num_classes in num_classes_list
        ])

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled_output = outputs.pooler_output
        logits = [classifier(pooled_output) for classifier in self.classifiers]
        proba = [F.softmax(logit, dim=1) for logit in logits]
        return proba
    


class MultiTaskDataset(Dataset):
    def __init__(self, texts, labels_list, tokenizer, max_len=128):
        self.texts = texts
        self.labels_list = labels_list
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):

        text = self.texts[idx]

        labels = [labels[idx] for labels in self.labels_list]

        encoding = self.tokenizer(text, add_special_tokens=True, max_length=self.max_len, padding='max_length', truncation=True, return_tensors='pt')
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0),
            'labels': labels
        }
    

data = pd.read_csv(file_path)
model_name = "google/canine-c"
texts = data['text'].values
task1_labels = list(data["is_relevant"].values)
task2_labels = list(data["object"].values)
task3_labels = list(data["is_positive"].values)

print(data.head())

tokenizer = AutoTokenizer.from_pretrained(model_name)

train_texts, val_texts, train_task1_labels, val_task1_labels, \
train_task2_labels, val_task2_labels, train_task3_labels, val_task3_labels = train_test_split(
    texts, task1_labels, task2_labels, task3_labels,
    test_size=0.1,
    stratify=task3_labels)


train_dataset = MultiTaskDataset(train_texts, [train_task1_labels, train_task2_labels, train_task3_labels], tokenizer)
val_dataset = MultiTaskDataset(val_texts, [val_task1_labels, val_task2_labels, val_task3_labels], tokenizer)

train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



model = MultiTaskBERT(model_name, [2, 3, 2]).to(device)
optimizer = AdamW(model.parameters(), lr=lr_start)
scheduler = ReduceLROnPlateau(optimizer, mode='max', factor=0.5, patience=5, verbose=True)


best_accuracy = 0.0
best_loss = float('inf')


train_losses_task = [[], [], []]
val_losses_task = [[], [], []]
train_accuracies = []
val_accuracies = []

for epoch in range(num_epochs):
    model.train()
    total_train_loss = 0.0
    losses_per_task = [0.0] * 3
    correct_counts = [0] * 3
    total_samples = 0

    for batch in train_loader:
        optimizer.zero_grad()
        logits = model(batch['input_ids'].to(device), batch['attention_mask'].to(device))
        losses = [nn.CrossEntropyLoss()(logits[i], batch['labels'][i].to(device)) for i in range(len(logits))]
        loss = sum(losses)
        loss.backward()
        optimizer.step()

        total_train_loss += loss.item()
        for i in range(3):
            losses_per_task[i] += losses[i].item()
            preds = torch.argmax(logits[i], dim=1)
            correct_counts[i] += (preds == batch['labels'][i].to(device)).sum().item()

        total_samples += batch['input_ids'].size(0)

    train_accuracy = sum(correct_counts) / (total_samples * len(logits))
    train_accuracies.append(train_accuracy)
    for i in range(3):
        train_losses_task[i].append(losses_per_task[i] / len(train_loader))

    print(f'Epoch {epoch+1}/{num_epochs}, Train Loss: {total_train_loss/len(train_loader):.4f}, Train Accuracy: {train_accuracy:.4f}')


    model.eval()
    total_val_loss = 0.0
    val_losses_per_task = [0.0] * 3
    correct_val_counts = [0] * 3
    val_samples = 0

    with torch.no_grad():
        for batch in val_loader:
            logits = model(batch['input_ids'].to(device), batch['attention_mask'].to(device))
            val_losses = [nn.CrossEntropyLoss()(logits[i], batch['labels'][i].to(device)) for i in range(len(logits))]
            total_val_loss += sum(val_losses).item()
            for i in range(3):
                val_losses_per_task[i] += val_losses[i].item()
                preds = torch.argmax(logits[i], dim=1)
                correct_val_counts[i] += (preds == batch['labels'][i].to(device)).sum().item()

            val_samples += batch['input_ids'].size(0)

    val_accuracy = sum(correct_val_counts) / (val_samples * len(logits))
    val_accuracies.append(val_accuracy)
    for i in range(3):
        val_losses_task[i].append(val_losses_per_task[i] / len(val_loader))

    print(f'Epoch {epoch+1}, Validation Loss: {total_val_loss/len(val_loader):.4f}, Validation Accuracy: {val_accuracy:.4f}')


    scheduler.step(val_accuracy)
    if val_accuracy > best_accuracy:
        best_accuracy = val_accuracy
        best_loss = total_val_loss / len(val_loader)
        torch.save(model.state_dict(), 'best_model.pth')
        print(f"Saved Best Model at Epoch {epoch + 1}")
