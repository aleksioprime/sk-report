# frontend: node + js
FROM node:lts-alpine as vue-build-stage

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install
COPY frontend ./

RUN npm run build

# backend: django and nginx
FROM python:3.7.6 as python-stage
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip

COPY ./backend/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip3 install gunicorn

COPY ./backend/entrypoint.sh ./
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]
COPY ./backend .

FROM nginx:1.22.1-alpine as prod-stage
WORKDIR /app

COPY --from=vue-build-stage /app/dist /usr/share/nginx/html
COPY ./nginx_default.conf /etc/nginx/conf.d/default.conf

CMD gunicorn --workers 4 --bind 0.0.0.0:5000 --daemon server:app \
  && sed -i -e "s/__PORT__/$PORT/" /etc/nginx/conf.d/default.conf \
  && nginx -g 'daemon off;'
