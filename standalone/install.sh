@echo off
echo "*** Installing django-ezybaas ***"
deactivate
rm -rf venv/
rm -rf ezybaasmain/
rm manage.py
virtualenv venv           
source venv/bin/activate
pip install -r requirements.txt
pip install django-ezybaas-0.1.0.tar.gz
django-admin startproject ezybaasmain .
echo # ** Following lines added by ezybaas install >> "ezybaasmain/settings.py"
echo "LOGIN_URL = 'login/'" >> "ezybaasmain/settings.py"
echo "INSTALLED_APPS += 'rest_framework'," >> "ezybaasmain/settings.py"
echo "INSTALLED_APPS += 'rest_framework_swagger'," >> "ezybaasmain/settings.py"
echo "INSTALLED_APPS += 'ezybaas'," >> "ezybaasmain/settings.py"
echo "from ezybaas.db import *" >> "ezybaasmain/settings.py"
echo "DATABASES['ezybaas']=EZYBAAS_DATABASES['ezybaas']" >> "ezybaasmain/settings.py"
echo "DATABASE_ROUTERS = ['ezybaas.db.EzyBaasDbRouter']" >> "ezybaasmain/settings.py"
echo "from django.urls import include" >> "ezybaasmain/urls.py"
#REM echo from ezybaas import urls >> "ezybaasmain/urls.py"
echo "urlpatterns += path('ezybaas/', include('ezybaas.urls'))," >> "ezybaasmain/urls.py"
python manage.py migrate
python manage.py migrate --run-syncdb --database ezybaas
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'default@ezybaas.com', 'admin')" | python manage.py shell
deactivate
echo "*** Installed django-ezybaas ***"
