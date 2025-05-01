# Базовый образ
FROM python:3.10-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    unzip \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libasound2 \
    libgbm1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем playwright-зависимости
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Устанавливаем браузеры для playwright
RUN python -m playwright install

# Копируем исходный код бота
COPY . /app
WORKDIR /app

# Команда запуска
CMD ["python", "main.py"]
