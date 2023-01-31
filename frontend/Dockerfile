# Указываем Docker использовать образ Node.js в качестве базового
FROM node:lts-alpine as build-vue
# Устанавливаем рабочий каталог контейнера 
WORKDIR /app
# Копируем файлы пакетов в контейнер и устанавливаем их
COPY frontend/package*.json ./
RUN npm install
# Копируем все файлы фронтенда и запускаем билд
COPY frontend ./
RUN npm run build
RUN ls -l
COPY --from=build-vue /app/dist /usr/share/nginx/html
# Запуск приложения
# CMD [ "npm", "run", "serve" ]
