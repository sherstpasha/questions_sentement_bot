import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset
from transformers import AutoModel, AutoTokenizer
from sklearn.model_selection import train_test_split
import torch.nn as nn
import matplotlib.pyplot as plt
import torch.nn.functional as F
import pandas as pd
import argparse


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
    

class PredictionDataset(Dataset):
    def __init__(self, texts, tokenizer, max_len=128):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        encoding = self.tokenizer(text, add_special_tokens=True, max_length=self.max_len, padding='max_length', truncation=True, return_tensors='pt')
        return {
            'input_ids': encoding['input_ids'].squeeze(0),
            'attention_mask': encoding['attention_mask'].squeeze(0)
        }
    

def load_model(model_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = MultiTaskBERT("google/canine-c", [2, 3, 2]).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))  # Ensure model is loaded to the correct device
    model.eval()
    return model

def get_predictions(model, dataloader, device):
    predictions = []
    with torch.no_grad():
        for batch in dataloader:
            logits = model(batch['input_ids'].to(device), batch['attention_mask'].to(device))
            batch_predictions = [torch.argmax(logit, dim=1).cpu().numpy() for logit in logits]
            predictions.extend(list(zip(*batch_predictions)))
    return predictions


parser = argparse.ArgumentParser(description='Run predictions with MultiTaskBERT')
parser.add_argument('--file_path', type=str, required=True, help='Path to the CSV file with texts')
parser.add_argument('--model_path', type=str, required=True, help='Path to the trained model file')
args = parser.parse_args()


file_path = args.file_path
model_path = args.model_path

data = pd.read_csv(file_path)
texts = data['text'].values

tokenizer = AutoTokenizer.from_pretrained("google/canine-c")
dataset = PredictionDataset(texts, tokenizer)
dataloader = DataLoader(dataset, batch_size=4, shuffle=False)

model = load_model(model_path)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

predictions = get_predictions(model, dataloader, device)

print(predictions)