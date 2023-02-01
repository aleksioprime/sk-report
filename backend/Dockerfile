# Указываем Docker использовать образ Python в качестве базового
FROM python:3.7.9
# Устанавливаем необходимые переменные окружения
ENV PYTHONUNBUFFERED 1
# Устанавливаем рабочий каталог контейнера 
RUN mkdir /backend
WORKDIR /backend
# Установка зависимостей
RUN pip install --upgrade pip
COPY backend/requirements.txt ./
EXPOSE 8000
RUN pip install -r requirements.txt
# Копируем все файлы из локального проекта в контейнер
COPY backend /backend/
