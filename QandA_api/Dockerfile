# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем системные зависимости для PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .


# Открываем порт 8000
EXPOSE 8000

# Запуск сервера (для production используйте Gunicorn)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
