# Используем официальный образ Python
FROM python:3.10-slim

# Обновляем пакеты и ставим системные зависимости (например, ffmpeg)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду, которая запускается по умолчанию
CMD ["python", "main.py"]
