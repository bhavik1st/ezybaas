mkdir d:\Test
cd d:\Test
virtualenv testenv            
call testenv\Scripts\activate
REM pip install --target=\Test -r requirements.txt
pip install Django==2.2.4
django-admin startproject ezybaasmain .
pip freeze > requirements.txt
REM pip install "D:\Susthitsoft\code\ezybaas\core\dist\django-ezybaas-0.1.0.tar.gz"
"DJANGO_SETTINGS_MODULE=<project-name>.settings.testing"

cd d:\Test\ezybaasmain
REM python manage.py migrate
REM python manage.py migrate --run-syncdb --database ezybaas
REM python manage.py createsuperuser
REM python manage.py runserver