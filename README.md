# Проект SKReport

## Backend

### Выгрузка приложения

1. Подготовка и выполнение миграций:
```
python manage.py makemigrations
python manage.py migrate
```
2. Создание суперпользователя:
```
python manage.py createsuperuser
superuser: alexprime
email: aleksioprime@gmail.com
password: A0Ru$$22
```
3. Импорт статических файлов:
```
python manage.py collectstatic
```
4. Загрузка фикстур в БД из JSON:
```
python manage.py loaddata data.json 
```
**Примечание.** Для формирования файла фикстур в Django можно выполнить команду:
```
python manage.py dumpdata > data.json 
python -Xutf8 manage.py dumpdata > data.json 
```
### Создание базы данных PostgreSQL

1. Открыть PSQL (в Linux - ввести *psql*, в Windows - открыть *SQL Shell*) из под администратора (например, с логином **postgre** и паролем **12345**)
2. Создать пользователя *igadmin* с паролем *Pox{@K*:
```
CREATE USER igadmin WITH PASSWORD 'Pox{@K';
```
3. Создать базу данных *igskolkovo* и дать все права к ней пользователю *igadmin*:
```
postgres=# CREATE DATABASE igskolkovo WITH owner=postgres ENCODING = 'UTF-8' lc_collate = 'en_US.utf8' lc_ctype = 'en_US.utf8' template template1;
postgres=# GRANT ALL PRIVILEGES ON DATABASE "igskolkovo" to igadmin;
```
**Примечание**
- Резервное копирования и восстановление данных из БД PostgreSQL:
```
pg_dump -U user_name database_name > file_name.dump
psql -U user_name database_name < file_name.dump
```
- Войти в БД и вывести таблицы:
```
\c igskolkovo
\dt
```
- Удалить базу данных:
```
DROP DATABASE <название базы>;
```
## Server
### Выполнение команд для backend при первом запуске:
```
docker exec -it CONTAINER_ID python3 manage.py migrate
docker exec -it CONTAINER_ID python3 manage.py createsuperuser
docker exec -it CONTAINER_ID python3 manage.py loaddata data.json 
```
### Обновление докеров на сервере:
```
docker-compose pull
docker-compose up
```
### Удаление всех контейнеров и образов:
```
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
```
