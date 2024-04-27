# Используем базовый образ Ubuntu с CUDA и cuDNN
FROM nvidia/cuda:12.4.1-runtime-ubuntu22.04

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    wget \
    git \
 && rm -rf /var/lib/apt/lists/*

# Установка библиотек CUDA и cuDNN
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcudnn8 \
    libcudnn8-dev \
 && rm -rf /var/lib/apt/lists/*

# Установка Python-зависимостей
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.10 get-pip.py
RUN rm get-pip.py
RUN pip3.10 install torch torchvision transformers scikit-learn pandas matplotlib

# Копирование исходного кода в контейнер
COPY . /app
WORKDIR /app

# Запуск обучения модели при сборке контейнера (можно изменить по вашему усмотрению)
CMD ["/bin/bash"]