@REM Запуск с помощью Docker
@REM 1. Установить Docker Desktop
@REM 2. В поиске контейнеров найти postgres, выбрать первый и нажать RUN
@REM 3. В открывшемся окне ввести необходимые данные (variables, volumes, поставить 0 в IP-адресе)
@REM 4. Запустить контейнер и номер внешнего порта скопировать в этот файл
@REM 5. Загрузить фикстуры: python manage.py loaddata --exclude contenttypes ../data/fixtures/data.json

@echo on
call "C:\venv\freshstream\Scripts\activate.bat"
set POSTGRES_PORT=32770
set POSTGRES_HOST=localhost
set POSTGRES_DB=igskolkovo
set POSTGRES_USER=igadmin
set POSTGRES_PASSWORD=Pox{@K
python manage.py runserver
pause
