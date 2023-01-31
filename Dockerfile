# frontend: node + js
FROM node:lts-alpine as vue-stage

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install
COPY frontend ./

RUN npm run build

# backend: django and nginx
FROM nginx:1.17.4 as prod-stage
WORKDIR /app

RUN apk update \
  && apk add --no-cache python3:~3.7 py3-pip\
  && pip3 install --upgrade pip setuptools wheel

COPY --from=vue-stage /app/dist /usr/share/nginx/html
COPY ./nginx_default.conf /etc/nginx/conf.d/default.conf

COPY ./backend/requirements.txt ./
RUN pip3 install -r requirements.txt --use-pep517
RUN pip3 install gunicorn

COPY ./backend/entrypoint.sh ./
RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]

COPY ./backend .

CMD gunicorn --workers 4 --bind 0.0.0.0:5000 --daemon server:app \
  && sed -i -e "s/__PORT__/$PORT/" /etc/nginx/conf.d/default.conf \
  && nginx -g 'daemon off;'
