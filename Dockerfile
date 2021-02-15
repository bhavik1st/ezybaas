FROM python:3.8-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gnupg npm \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip

WORKDIR /usr/src/app
COPY core .
#RUN pip install -r requirements.txt
RUN cd /usr/src/app/ezybaas/static && npm -v && npm install 
RUN cd /usr/src/app && python -m pip install -r requirements.txt
RUN python manage.py makemigrations 
RUN python manage.py migrate 
RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@ezybaas.com', 'admin')" | python manage.py shell
EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "ezybaasmain.wsgi:application"]

#WORKDIR /usr/src/app
#COPY core .
#RUN pip install -r requirements.txt

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



