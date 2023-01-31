# Указываем Docker использовать образ Python в качестве базового
FROM python:3.7.6
# FROM nginx:1.17.4-alpine
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
RUN ls -l
COPY backend/nginx_default.conf /etc/nginx/conf.d/default.conf

RUN pip3 install gunicorn
CMD gunicorn --workers 4 --bind 0.0.0.0:5000 --daemon server:app \
  && sed -i -e "s/__PORT__/$PORT/" /etc/nginx/conf.d/default.conf \
  && nginx -g 'daemon off;'