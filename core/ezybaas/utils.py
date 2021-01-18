# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.

import os
from . import config
from django.apps import apps
from .models import App,Table,MetaModel
from . import baas
from django.core import management
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_app(app):
	allApps = get_apps_dict()

	for allApp in allApps:
		if allApp['name']==app:
			return allApp	
	return {}

def get_apps_old():
	final_apps = []
	
	installed_apps = settings.INSTALLED_APPS	#contains all apps in INSTALLED_APPS
	direc = os.path.dirname(__file__)
	file_path = os.path.abspath(os.path.join(baas.return_project(), '..'))
	
	file_path = os.listdir(file_path)

	# intesection
	final_apps = [app for app in installed_apps if app in file_path] 
	
	final_apps=remove_baasname(final_apps)

	logger.info('Apps returned')
	return final_apps

def get_apps():
	apps = App.objects.all()
	return apps

def remove_baasname(apps):
	#Function to remove Djbaas from the list of all Apps
	if any('djbaas' in app for app in apps):
		apps.remove('djbaas')
	if any('djbaas.apps.DjbaasConfig' in app for app in apps):
		apps.remove('djbaas.apps.DjbaasConfig')

	if any('ezybaas' in app for app in apps):
		apps.remove('ezybaas')
	if any('ezybaas.apps.EzybaasConfig' in app for app in apps):
		apps.remove('ezybaas.apps.EzybaasConfig')

	return apps
def get_apps_dict():
	apps = get_apps()
	apps_dict = []

	i=1
	for app in apps:
		app_dict = {
			"name" : app,
			"id" : i,
		}
		apps_dict.append(app_dict)
		i=i+1

	return apps_dict

def populate_index_table():
	apps = get_apps()
	data = []
	for app in apps:
		tables = get_models(app)
		obj ={
			"name" : app,
			"tables" : tables,
			"count_tables" : len(tables),
			"fields" : len(MetaModel.objects.filter(app=app).values()),
			"authentication" : app.auth,
			"version" :app.version,
			"status" :app.active
		}
		data.append(obj)
	return data

def get_models(app):
	my_models = apps.all_models[app]
	list_keys_models = [ k for k in my_models ]
	return list_keys_models

def get_all_tables():
	tables = []
	apps = get_apps()
	for app in apps:
		tables += get_models(app)
	return tables

def get_fields(app,table = None):
	if table == None:
		obj = MetaModel.objects.filter(app=app).values()
	else:
		obj = MetaModel.objects.filter(app=app, table=table).values()
	return obj

def get_tables_old(app):
	all_fields = get_fields(app)
	tables = []
		
	for obj in all_fields:
		if not obj['table'] in tables:
			tables.append(obj['table'])
	
	logger.info('Returns Tables')
	return tables
	
def get_tables(app=None):
	if app==None:
		tables_query = Table.objects.filter().values()
	else:
		tables_query = Table.objects.filter(app=app).values()
	
	tables = []
	for table in tables_query:
		tables.append(table['name'])
	return tables

def check_none(value,  attribute):
	if value == "None":
		return ""
	else:
		return str(attribute) + "=" + str(value) + ", "


