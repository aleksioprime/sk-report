# Проект SKReport

## Запуск приложения у разработчика
### Подготовка базы данных
1. Установить PostgreSQL (https://www.postgresql.org/download/)
2. Открыть PSQL (в Linux - ввести *psql*, в Windows - открыть *SQL Shell*) из под администратора (например, с логином **postgre** и паролем **12345**)
3. Создать пользователя *igadmin* с паролем *Pox{@K*:
```
CREATE USER igadmin WITH PASSWORD 'Pox{@K';
```
4. Создать базу данных *igskolkovo* и дать все права к ней пользователю *igadmin*:
```
postgres=# CREATE DATABASE igskolkovo WITH owner=postgres ENCODING = 'UTF-8' lc_collate = 'en_US.utf8' lc_ctype = 'en_US.utf8' template template1;
postgres=# GRANT ALL PRIVILEGES ON DATABASE "igskolkovo" to igadmin;
```
### Запуск бэкенда:
1. Создать каталог на локальном компьютере и загрузить в него репозиторий через команды **Code -> Download ZIP** или через команду терминала:
```
git clone https://https://github.com/aleksioprime/igskolkovo
```
2. Установить виртуальное окружение для Python (используется версия 3.7.9):
```
pip install virtualenv
python -m venv <название каталога>
```
Примечание. В MacOS используются команды *pip3* и *python3*
3. Запустить виртуальное окружение и установить все зависимости в backend'е.
Для MacOS:
```
source <название каталога>/bin/activate
pip3 install -r requirements.txt
```
Для Windows:
```
<название каталога>\Scripts\activate.bat
pip install -r requirements.txt
```
4. Установить переменные виртуальное окружения для подключения к базе данных:
```
set POSTGRES_PORT=5432
set POSTGRES_HOST=localhost
set POSTGRES_DB=igskolkovo
set POSTGRES_USER=igadmin
set POSTGRES_PASSWORD=Pox{@K
```
5. Перейти в каталог бэкенда в терминале, подготовить и выполнить миграции:
```
python manage.py makemigrations
python manage.py migrate
```
6. Создать суперпользователя (возможно пропустить при наличии фикстур):
```
python manage.py createsuperuser
superuser: alexprime
email: aleksioprime@gmail.com
password: A0Ru$$22
```
7. Импортировать статические файлы:
```
python manage.py collectstatic
```
8. Загрузить фикстуры в БД из JSON:
```
python manage.py loaddata data.json 
```
**Примечание.** Для формирования файла фикстур в Django можно выполнить команду:
```
python manage.py dumpdata > data.json 
python -Xutf8 manage.py dumpdata > data.json 
```
9. Запустить сервер Django
```
python manage.py runserver
```

### Запуск фронтенда:
1. Перейти в каталог фронтенда в терминале и установить окружение:
```
npm install
```
2. Скомпилировать файлы проекта:
```
npm run build
```
3. Запустить сервер Vue:
```
npm run serve
```

## Запуск приложения на сервере

1. Установить сервер на Ubintu (текущая версия 20.04) с Docker из маркетплейса
2. Загрузить папку *devops* на сервер в домашний каталог
3. Подключиться к серверу и перейти в каталог *devops*:
```
cd devops
```
4. Запустить docker-compose:
```
docker-compose up
```
Примечание. Образы проекта автоматически компилируются в Docker Hub. Для обновления проекта на сервере нужно загружать их оттуда заново:
```
docker-compose pull
``` 
5. При первом запуска или обновлении структуры БД посмотреть ID контейнера бекенда и выполнить команды:
```
docker ps
docker exec -it CONTAINER_ID python3 manage.py migrate
docker exec -it CONTAINER_ID python3 manage.py loaddata data.json 
```

## Справочные материалы
### Работа в PostgreSQL
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
### Работа с Docker
- Удаление всех контейнеров и образов:
```
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
```
