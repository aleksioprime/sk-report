# Указываем Docker использовать образ Node.js в качестве базового
FROM node:lts-alpine
# Устанавливаем рабочий каталог контейнера 
WORKDIR /usr/src/app
# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package*.json ./
RUN npm install
# Копируем все файлы фронтенда и запускаем билд
COPY frontend ./
RUN npm run build

COPY dist /usr/share/nginx/html
# Запуск приложения
# CMD [ "npm", "run", "serve" ]
