# Базовый образ с поддержкой Playwright и Python 3.10
FROM mcr.microsoft.com/playwright/python:v1.42.0

# Рабочая директория
WORKDIR /app

# Копируем проект в контейнер
COPY . .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем main.py (в aiogram 2.x)
CMD ["python", "main.py"]
