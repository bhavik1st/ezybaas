# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.
 
from . import config
from . import constants
from . import utils
from . import baas

import subprocess


import platform
import datetime
from django.core import management


from .models import MetaModel, App, Table, Config, DbSettings, Version
from .serializers import MetaModelSerializer, AppSerializer, TableSerializer, ConfigSerializer, VersionSerializer, DbSettingsSerializer
from . import views

from django.http import HttpResponse
import json
import sys
import os
import re
import pdb
from django.core import management
from django.conf import settings
from rest_framework.parsers import JSONParser
# from django.core.management import call_command
from django.shortcuts import render
from django.http import Http404
from django.contrib import messages  # Messages

#from django.db.models import get_app, get_models
from django.apps import apps
from .utils import get_models


# Rest Framework
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# Auth
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import permissions
#from rest_framework.permissions import IsAuthenticated

# For checking user permission
from django.contrib.auth.mixins import UserPassesTestMixin

# Neccessary for Session Auth


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class IsSuperUser(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


# AUTH_CLASSES = [CsrfExemptSessionAuthentication]
AUTH_CLASSES = [TokenAuthentication,
                BasicAuthentication, CsrfExemptSessionAuthentication]
PERM_CLASSES = [IsAuthenticated, IsSuperUser]


class VersionAPI(APIView):
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    # TODO: Fix Auth Error here

    def get(self, request, format=None):
        version = Version()
        serializer = VersionSerializer(version)
        return Response(serializer.data)

# Api for dump and load data from database.
class ImportExportAPI(APIView):
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES

    def get(self, request, format=None):
        try:
            app = App.objects.all()
            for appname in app:
                if appname == " " or appname == 'none':
                    return HttpResponse({'message': 'No such app found'})
                else:
                    sys.stdout = open('ezybaas'+'.json', 'w')
                    management.call_command('dumpdata', '--database', 'ezybaas')
                    # sys.stdout.close()


            with open('ezybaas.json', 'r+') as jsondata:
                data = jsondata.read()
            return HttpResponse(data, content_type='application/json')
        except Exception as e:
            content = {'message': str(e)}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        data = request.data
        try:
            if data == {} or data is None or data == []:
                content = {'message': 'Input data is invalid or null!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                for element in data:  # Root Array
                    if element["model"] == "ezybaas.app":
                        element["fields"]["dirty"] = True

                with open("ezybaas.json", "w") as jsonfile:
                    json.dump(data, jsonfile)

                management.call_command('loaddata', '--database', 'ezybaas', 'ezybaas.json')
                content = {'message': 'Import Successful!'}
                return Response(content, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StatusAPI(APIView):

    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    def get(self, request, appname=None):

        apps = App.objects.all()
        app_status = []

        def active_api(app):
            api_response = {
                "active": True,
                "app": app.name,
                "auth": app.auth,
                "created": app.created,
                "modified": app.modified,
                "api": app.api,
                # "active": app.active,
                "dirty": app.dirty,
                "version": app.version,
            }
            return api_response

        def inactive_api(app):
            api_response = {
                "active": False,
                "app": app.name,
                "auth": app.auth,
                "created": app.created,
                "modified": app.modified,
                "api": app.api,
                # "active":app.active,
                "dirty": app.dirty,
                "version": app.version,
            }
            return api_response

        try:
            if appname == None:
                for app in apps:
                    if str(app) in settings.INSTALLED_APPS:
                        api_response = active_api(app)
                        app_status.append(api_response)
                    else:
                        api_response = inactive_api(app)
                        app_status.append(api_response)
                return Response(app_status, status=status.HTTP_200_OK)
            else:
                # return only one
                for app in apps:
                    if str(app) == appname:
                        app = app
                    else:
                        content = {'message': appname + ' Is Not Found !'}
                        return Response(content, status=status.HTTP_400_BAD_REQUEST)

                if appname in settings.INSTALLED_APPS:
                    api_response = active_api(app)
                    app_status.append(api_response)
                else:
                    api_response = inactive_api(app)
                    app_status.append(api_response)

                return Response(app_status, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message': str(e)}
        return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, appname=None):

        data = request.data
        app_folders = os.listdir(os.getcwd())
        app_status = []

        try:
            if data == {} or data is None or data == []:
                content = {'message': 'Input data is invalid or null!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                for apps in data:
                    app = str(apps['app'])
                    model = get_models(app)

                    if app in settings.INSTALLED_APPS:
                        content = {'message': app+' App is already active!'}
                        app_status.append(content)

                    elif app not in app_folders:
                        content = {'message': app +
                                   ' App folder is not created!'}
                        app_status.append(content)

                    elif model in app_models is None:
                        content = {'message': app+' has no model!'}
                        app_status.append(content)

                    else:
                        # baas.create_app(str(data['appname']))
                        baas.update_settings(str(data['appname']))
                        content = {'message': app+' App Add Successful!'}

                return Response(app_status, status=status.HTTP_200_OK)

        except Exception as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class apiLiveAPI(APIView):

    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES

    def post(self, request, format=None):
        data = request.data
        try:
            if data == {} or data is None or data == []:
                content = {'message': 'Input data is invalid or null!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                app = str(data['app'])
                if app:
                    baas.go_live(app)
                    # management.call_command('makemigrations',app)
                    # management.call_command('migrate')
                    
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
class  migrateApp(APIView):
    
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES

    def post(self, request, format=None):
        data = request.data
        try:
            if data == {} or data is None or data == []:
                content = {'message': 'Input data is invalid or null!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                app = str(data['app'])
                if app:
                    obj = App.objects.get(name=app)
                    obj.active = True
                    obj.save()
                    management.call_command('makemigrations',app)
                    management.call_command('migrate')
                    # baas.make_migrations(app)
                    # bass.migrate_changes
                    
                return Response(status=status.HTTP_200_OK)

        except Exception as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    


class DeleteAPI(APIView):

    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    def get(self, request, appname=None):

        app = str(appname)
        apps = App.objects.all()
        app_folders = os.listdir(os.getcwd())

        try:
            if app == {} or app is None or app == []:
                content = {'message': 'Input data is invalid or null!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

            else:
                for i in apps:
                    if str(i) == app or app in app_folders:
                        baas.delete_app(app)
                        app_obj = App.objects.filter(name=app).delete()
                        content = {'message': app+' App Delete Successful!'}
                        return Response(content, status=status.HTTP_200_OK)

                if app not in app_folders:
                    content = {'message': app+' App Not Found!'}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MonitoringAPI(APIView):

    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES

    def get(self, request, format=None):
        try:
            response = {
                'python':
                {'compiler': platform.python_compiler(), 'implementation': platform.python_implementation(
                ), 'version': platform.python_version(), 'build': platform.python_build()},
                    'system':
                {'architecture': platform.architecture(), 'machine': platform.machine(), 'node': platform.node(), 'platform': platform.platform(), 'processor': platform.processor(),
                 'release': platform.release(), 'os': platform.system(), 'version': platform.version()}
            }

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DBactiveAPI(APIView):

    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES

    def post(self, request):
        data = request.data
        try:
            if data == {} or data is None or data == []:
                content = {'message': 'Input data is invalid or null!'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                dbs = DbSettings.objects.all()
                for db in dbs:
                    if data['key'] not in db.key:
                        db.active = False 
                        db.save()
                        # baas.make_migrations()
                    # elif data['key'] == 'default':
                    # 	activedb = data['key']
                    # 	db.active = True
                    # 	db.save()
                    # 	content = {'message': activedb +' is Active'}
                    else:
                        db.active = True
                        db.save()
                        # if data.key is present in dbsettings then it  remove from settings.py
                        x ="DATABASES['default']=EZYBAAS_DATABASES"
                        def return_project():
                            return os.environ['DJANGO_SETTINGS_MODULE'].split('.')[0]
                        settings_file = os.path.abspath(os.path.join(baas.return_project(), 'settings.py'))

                        file = open(settings_file, 'r')
                        lines = file.readlines()
                        file.close()

                        file = open(settings_file, 'w')
                        for line in lines:
                            if x in line:
                                continue
                            else:
                                file.write(line)

                        file.close()

                        #Add in Settings.py
                        activedb = data['key']
                        if activedb == 'default':
                            settings_file = os.path.abspath(os.path.join(return_project(), 'settings.py'))
                            management.call_command('makemigrations')
                            management.call_command('migrate')
                            content = {'message': activedb+" is Active"}
                        else:
                            settings_file = os.path.abspath(os.path.join(return_project(), 'settings.py'))
                            file = open(settings_file, 'a')

                            updated_settings = "\n\nDATABASES['default']=EZYBAAS_DATABASES['{0}']".format(str(activedb))

                            file.write(updated_settings)
                            file.close()

                            #migrate Databases
                            management.call_command('makemigrations')
                            management.call_command('migrate')


                        content = {'message': activedb+" is Active"}
                return Response(content, status=status.HTTP_200_OK)

        except Exception as e:
            content = {'message': str(e)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DbSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    queryset = DbSettings.objects.all()
    serializer_class = DbSettingsSerializer


class ConfigViewSet(viewsets.ModelViewSet):
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer


class AppViewSet(viewsets.ModelViewSet):
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    queryset = App.objects.all()
    serializer_class = AppSerializer


class TableViewSet(viewsets.ModelViewSet):
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class FieldViewSet(viewsets.ModelViewSet):
    permission_classes = PERM_CLASSES
    authentication_classes = AUTH_CLASSES
    queryset = MetaModel.objects.all()
    serializer_class = MetaModelSerializer
