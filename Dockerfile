# Используем официальный образ Python из Docker Hub
FROM python:3.9-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаем и устанавливаем рабочий каталог
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    && apt-get clean

# Копируем файл зависимостей и устанавливаем их
COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt

# Копируем файлы вашего проекта в контейнер
COPY . /app/

# Создаем миграции и применяем их
RUN python3 currency_tracker/manage.py makemigrations
RUN python3 currency_tracker/manage.py migrate

# Запускаем сервер, Celery Beat и Celery Worker
CMD ["sh", "-c", "python3 currency_tracker/manage.py runserver 0.0.0.0:9999 && celery -A currency_tracker beat -l info && celery -A currency_tracker worker -l info"]
