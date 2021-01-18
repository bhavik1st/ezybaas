# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.

import os
from . import appslist
from django.conf import settings

BASE_DIR = settings.BASE_DIR
EZYBAAS_DATABASES = {
    'production': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'ezybaas.prod.db'),
    },
    'staging': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'ezybaas.staging.db'),
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'ezybaas.test.db'),
    },
    'ezybaas': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'ezybaas.db'),
    }
}

DATABASE_APPS_MAPPING = {'contenttypes': 'default',
                     'auth': 'default',
                     'admin': 'default',
                     'sessions': 'default',
                     'messages': 'default',
                     'staticfiles': 'default',
                     'ezybaas': 'ezybaas',
                     }

class EzyBaasDbRouter:

    def db_for_read(self, model, **hints):
            if model._meta.app_label == 'ezybaas':
                return 'ezybaas'
            return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'ezybaas':
            return 'ezybaas'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        if (obj1._meta.app_label == 'ezybaas' and
            obj2._meta.app_label == 'ezybaas'):
           return True
        elif (obj1._meta.app_label != 'ezybaas' and
              obj2._meta.app_label != 'ezybaas'):
           return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if db == 'ezybaas':
            return app_label == 'ezybaas'
        elif app_label == 'ezybaas':
            return db == 'ezybaas'

        return True

        