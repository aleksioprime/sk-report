# Указываем Docker использовать образ Python в качестве базового
FROM python:3.7.6
# Устанавливаем рабочий каталог контейнера 
WORKDIR /usr/src/app
# Устанавливаем необходимые переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Установка зависимостей
RUN pip install --upgrade pip
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
# Копируем все файлы из локального проекта в контейнер
COPY backend ./
# Запуск проекта
# ENTRYPOINT ["python3"] 
# CMD ["manage.py", "runserver"]