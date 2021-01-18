@ECHO off
:STEP1
REM  Step 1 - Install npm packages
REM  Needs node and npm to be pre-installed
cd core\ezybaas\static
echo %CD%
CALL npm install && ECHO "Installed NPM Packages" || ECHO "Failed installing packages"
GOTO STEP2

:STEP2
REM  Step 2 - Setup Django Dependencies
REM  Needs pip and virtualenv to be pre-installed.
cd ..
cd ..
echo %CD%
ECHO "Create or Reuse venv"
IF NOT EXIST "venv" ( 
virtualenv venv
)
CALL venv\Scripts\activate
pip install -r requirements.txt

REM  Step 3 - Create default database (Sqlite)
REM  Needs pip and virtualenv to be pre-installed.
python manage.py makemigrations
python manage.py migrate

REM  Step 4 - Create superuser for login to ezybaas
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@ezybaas.com', 'admin')" | python manage.py shell
REM python manage.py createsuperuser --noinput --username admin --email admin@ezybaas.com

REM  Step 5 - Run D
REM  Run Django on localhost:8000 (default)
python manage.py runserver
