# Указываем Docker использовать образ Python в качестве базового
FROM python:3.7.6
# Устанавливаем рабочий каталог контейнера 
WORKDIR /usr/src/app
# Устанавливаем необходимые переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
# Установка зависимостей
RUN pip install --upgrade pip
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
# Копируем все файлы из локального проекта в контейнер
COPY ./backend ./