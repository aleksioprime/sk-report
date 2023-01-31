# Указываем Docker использовать образ Node.js в качестве базового
FROM node:lts-alpine
# Устанавливаем рабочий каталог контейнера 
WORKDIR /app
# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package*.json ./
RUN npm install
RUN ls -l
# Копируем все файлы фронтенда и запускаем билд
COPY frontend ./
RUN ls -l
RUN npm run build
RUN ls -l
COPY /app/dist /usr/share/nginx/html
# Запуск приложения
# CMD [ "npm", "run", "serve" ]
