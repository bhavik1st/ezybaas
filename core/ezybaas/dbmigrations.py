from django.db import migrations
from django.db import models
from datetime import datetime
from django.apps import apps

null = "null"
false = "false"
true = "true"

databases = [
    {

        "pk": "default",
        "type": "SQLITE",
        "name": "ezybaas.db",
        "user": null,
        "password": null,
        "host": null,
        "port": null,
        "active": false

    },
    {

        "pk": "ezybaas",
        "type": "SQLITE",
        "name": "ezybaas.db",
        "user": null,
        "password": null,
        "host": null,
        "port": null,
        "active": false,

    },
    {

        "pk": "production",
        "type": "SQLITE",
        "name": "ezybaas.prod.db",
        "user": "NONE",
        "password": "NONE",
        "host": "NONE",
        "port": "NONE",
        "active": false,

    },
    {

        "pk": "staging",
        "type": "SQLITE",
        "name": "ezybaas.staging.db",
        "user": "nnnn",
        "password": null,
        "host": "NONE",
        "port": null,
        "active": true,

    },
    {
        "pk": "test",
        "type": "SQLITE",
        "name": "ezybaas.test.db",
        "user": "admin",
        "password": null,
        "host": "local",
        "port": "3306",
        "active": false,

    }
]


def DB_Connection(apps, schema_editor):
  
    DB_Connections = apps.get_model('ezybaas', 'dbsettings')
    for db in DB_Connections.objects.all():
        if db <= 0:
            for i in range(4):
                for k,v in databases[i].items():
                    console.log(k,v)
                    DB_Connections.objects.create(key= v,
                        type= v,
                        name= v,
                        user= v,
                        password= v,
                        host= v,
                        port= v,
                        active= v,
                    )


class Migration(migrations.Migration):

    dependencies = [
        ('ezybaas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(DB_Connection),
    ]
