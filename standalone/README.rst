ezybaas
-----------

ezybaas is a simple Django app to create RESTful APIs without writing any Server Side Code.
Detailed documentation is in the docs directory.

Quick start
-----------



1. Add ezybaas to your INSTALLED_APPS setting like this:
pip install ezybaas

	INSTALLED_APPS = [
	...	
	'ezybaas',
	'rest_framework',
	'rest_framework_swagger',
	]


3. Run `python manage.py migrate` to create the ezybaas models.

4. Run 'python manage.py loaddata --database ezybaas ezybaas/db.json'

5. Run 'python manage.py migrate --run-syncdb --database ezybaas'

6. Start the development server and visit http://127.0.0.1:8000/admin/ (you'll need the Admin app enabled).

7. Visit http://127.0.0.1:8000/ezybaas/.

8. Create superuser 
