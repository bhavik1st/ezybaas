# Step 1 - Install npm packages
# Needs node and npm to be pre-installed
cd ezybaas/static
npm install

# Step 2 - Setup Django Dependencies
# Needs pip and virtualenv to be pre-installed.
cd ..
cd ..
if [! -d "$DIR" ]; then
    virtualenv venv

source venv/bin/activate
pip install -r requirements.txt

# Step 3 - Create default database (Sqlite)
# Needs pip and virtualenv to be pre-installed.
python manage.py makemigrations
python manage.py migrate

# Step 4 - Create superuser for login to ezybaas
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@ezybaas.com', 'admin')" | python manage.py shell
#python manage.py createsuperuser --noinput --username admin --email admin@ezybaas.com