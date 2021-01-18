# ezybaas

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Django>= 2.2.4](https://img.shields.io/badge/django-2.2.4-blue.svg)](https://www.djangoproject.com/download/)
[![djangorestframework>= 3.9.4](https://img.shields.io/badge/djangorestframework-3.9.4-blue.svg)](https://www.django-rest-framework.org/)
[![django-rest-swagger>=2.2.0](https://img.shields.io/badge/djangorestswagger-2.2.0-blue.svg)](https://django-rest-swagger.readthedocs.io/en/latest/)

## EzyBaaS - Easiest Backend as a Service.

Take your idea to API in minutes.
* No Coding required. 
* Works with any SQL DB (MySQL, PostGresDB, MariaDB, SQLite, OracleDB)
* Deploy anywhere (Cloud Ready) 
* Flexible & Customizable 
* GraphQL APIs (Coming Soon)

## Getting Started 
* You can use ezybaas as standalone microservice.
* You can also use ezybaas as a django plugin in your project.

### Prerequisites
1. pip install ezybaas

2. Add ezybaas to your INSTALLED_APPS setting like this:
```
    INSTALLED_APPS = [
        ...	
        'ezybaas',
        'rest_framework',
        'rest_framework_swagger',
        ]
```
3. Include the ezybaas URLconf in your project urls.py like this:
```
    from django.urls import path,include
```
```
	path('ezybaas/', include('ezybaas.urls')),
```
4. Add these lines at the end of Settings.py

```
	LOGIN_URL = 'login/'
```
```
	from ezybaas.db import *
	DATABASES['ezybaas']=EZYBAAS_DATABASES['ezybaas']
	DATABASE_ROUTERS = ['ezybaas.db.EzyBaasDbRouter']
```

5. Run `python manage.py migrate` to create the ezybaas models.

6. Run `python manage.py loaddata --database testenv/Lib/site-packages/ezybaas/static/db.json`
<!-- 4. Run `python manage.py loaddata --database ezybaas ezybaas/db.json` -->

7. Run `python manage.py migrate --run-syncdb --database ezybaas`

8. Create superuser 

9. Start the development server and visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (you'll need the Admin app enabled).

10. Visit [http://127.0.0.1:8000/ezybaas/](http://127.0.0.1:8000/ezybaas/).


## Authors

* **Bhavik Shah** - Founder & CTO of *Susthitsoft Technologies Private Limited*


## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details





