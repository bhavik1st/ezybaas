# Step 1 - Install npm packages
# Needs node and npm to be pre-installed
cd core/ezybaas/static
npm install

# Step 2 - Setup Django Dependencies
# Needs pip and virtualenv to be pre-installed.
cd ../..
[ -d "venv" ] && echo "venv already exists!" || virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Step 3 - Create default database (Sqlite)
# Needs pip and virtualenv to be pre-installed.
python manage.py makemigrations
python manage.py migrate

# Step 4 - Create superuser for login to ezybaas
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@ezybaas.com', 'admin')" | python manage.py shell
#python manage.py createsuperuser --noinput --username admin --email admin@ezybaas.com

# Step 5 - Run D
# Run Django on localhost:8000 (default)
python manage.py runserver
