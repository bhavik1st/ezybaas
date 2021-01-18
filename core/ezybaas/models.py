# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.

from django.db import models
from . import constants
from . import config
from datetime import datetime

class Version(object):
	def __init__(self):
		self.name = config.EZYBAAS_RELEASE_NAME
		self.author = config.EZYBAAS_RELEASE_AUTHOR
		self.version = config.EZYBAAS_RELEASE_VERSION
		self.releasenotes = config.EZYBAAS_RELEASE_NOTES
		self.releasedate = config.EZYBAAS_RELEASE_DATE
		self.standalone = config.EZYBAAS_RELEASE_STANDALONE
		self.license = config.EZYBAAS_RELEASE_LICENSE
		self.now = datetime.now()

# ASPER - https://docs.djangoproject.com/en/2.2/ref/settings/#databases
class DbSettings(models.Model):
	engines = (
							('SQLITE', 'SQLite'),
							('POSTGRES', 'Postgres'),
							('MySQL', 'MySQL'),
							('MARIADB', 'Maria'),
							('ORACLE', 'Oracle'),
							('OTHER', 'Other'),
			  )

	key = models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=True, unique=True, blank=False, null=False, default='default')
	type =  models.CharField(max_length=constants.FIELD_MAX_LENGTH, choices=engines, primary_key=False, unique=False, blank=False, null=False)
	name =  models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=False, unique=False, blank=False, null=False)
	user = models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=False, unique=False, blank=False, null=True)
	password = models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=False, unique=False, blank=False, null=True)
	host = models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=False, unique=False, blank=False, null=True)
	port = models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=False, unique=False, blank=False, null=True)
	atomic = models.BooleanField(blank=False, null=False, default=False)
	commit = models.BooleanField(blank=False, null=False, default=True)
	active = models.BooleanField(blank=False, null=False, default=False)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name


class Config(models.Model):
	key = models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=True, unique=True, blank = False, null = False)
	value = models.CharField(max_length=constants.FIELD_MAX_LARGE, primary_key=False, unique=False, blank=True, null=True)
	
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.key


class App(models.Model):
	auth_choices = (
		('NONE','No Authentication'),
		('BASIC','Basic Authentication'),
		('SESSION','Session Authentication'),
		('TOKEN','Token Authentication'),
		('SOCIAL','Social Authentication')
	)
	name = models.CharField(max_length=constants.FIELD_MAX_LENGTH, primary_key=True, unique=True, blank = False, null = False)
	description = models.CharField(max_length=constants.FIELD_MAX_LARGE, default='', blank = True, null = True)
	auth = models.CharField(max_length=64, blank=False, null=False, choices=auth_choices, default="NONE")	
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	api = models.BooleanField(blank=False, null=False, default=True)
	active = models.BooleanField(blank=False, null=False, default=False)
	dirty = models.BooleanField(blank=False, null=False, default=False)
	version = models.IntegerField(blank=False, null=False, default=0)

	# :TODO These are Advanced Features, not implemented yet.
	auditlog = models.BooleanField(blank=False, null=False, default=False)
	graphql = models.BooleanField(blank=False, null=False, default=False)
	
	def __str__(self):
		return self.name


class Table(models.Model):

	# Key = appName:TableName
	key = models.CharField(max_length=constants.FIELD_MAX_LARGE, primary_key=True)
	name = models.CharField(max_length=constants.FIELD_MAX_LENGTH, blank = False, null = False)
	api = models.BooleanField(blank=False, null=False, default=True)
	owneraccess = models.BooleanField(blank=False, null=False, default=False)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	app = models.ForeignKey('App', on_delete=models.CASCADE,)
		
	# :TODO These are Advanced Features, not implemented yet.
	pagination = models.BooleanField(blank=False, null=False, default=False)
	# Serliazer 
	# Expose in API

	# For Authentication and RBAC in generated rest API.py check alternatives like
	# https://github.com/computer-lab/django-rest-framework-roles
	# And one using django guardian object permissions middleware
	# https://neolithic.blog/2017/12/03/rbac-with-django-rest-framework/
	
	def __str__(self):
		return self.name


class MetaModel(models.Model):
	field_choices = (
							('AutoField', 'AutoField'),
							('BigAutoField', 'BigAutoField'),
							('BigIntegerField', 'BigIntegerField'),
							('BinaryField', 'BinaryField'),
							('BooleanField', 'BooleanField'),
							('CharField', 'CharField'),
							('DateField', 'DateField'),
							('DateTimeField', 'DateTimeField'),
							('DecimalField', 'DecimalField'),
							('DurationField', 'DurationField'),
							('EmailField', 'EmailField'),
							('ForeignKey', 'ForeignKey'),
							('FileField', 'FileField'),
							('FilePathField', 'FilePathField'),
							('FloatField', 'FloatField'),
							('GenericIPAddressField', 'GenericIPAddressField'),
							('ImageField', 'ImageField'),
							('IntegerField', 'IntegerField'),
							('ManyToManyField', 'ManyToManyField'),
							('nullBooleanField', 'nullBooleanField'),
							('OneToOneField', 'OneToOneField'),
							('PositiveIntegerField', 'PositiveIntegerField'),
							('PositiveSmallIntegerField', 'PositiveSmallIntegerField'),
							('SlugField', 'SlugField'),
							('SmallIntegerField', 'SmallIntegerField'),
							('TextField', 'TextField'),
							('TimeField', 'TimeField'),
							('URLField', 'URLField'),
							('UUIDField', 'UUIDField'),
						)
	foreignkey_on_delete = (
							('No Foreign Key', 'No Foreign Key'),
							('CASCADE', 'CASCADE'),
							('PROTECT', 'PROTECT'),
							('SET_NULL', 'SET_NULL'),
							('SET_DEFAULT', 'SET_DEFAULT'),
						)

	app = models.ForeignKey('App', on_delete=models.CASCADE,)
	table = models.CharField(max_length=constants.FIELD_MAX_LENGTH, blank=False, null=False)
	tablekey = models.ForeignKey('Table', on_delete=models.CASCADE,)
	name = models.CharField(max_length=constants.FIELD_MAX_LENGTH, blank=False, null=False)
	type = models.CharField(max_length=64, blank=False, null=False, choices=field_choices,default="CharField")
	null = models.BooleanField(blank=True, null=True, default=True)
	blank = models.BooleanField(blank=True, null=True, default=True)
	default = models.CharField(max_length=constants.FIELD_MAX_LENGTH, blank=True, null=True, default=None)
	min = models.IntegerField(blank=True, null=True, default=-1)
	max = models.IntegerField(blank=True, null=True, default=constants.FIELD_MAX_LENGTH)
	unique = models.BooleanField(blank=True, null=True, default=False)
	primarykey = models.BooleanField(blank=True,null=True, default=False)
	foreignkeytable = models.CharField(max_length=constants.FIELD_MAX_LENGTH, blank=True, null=True, default=None)
	ondelete = models.CharField(max_length=100, blank=True, choices = foreignkey_on_delete, default = "No Foreign Key")
	inapi = models.BooleanField(blank=True, null=True, default=True)
	version = models.IntegerField(blank=True, null=True, default=0)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	# :TODO Remove expose from field level

	def __str__(self):
		return self.app.name + '_' + self.table + '_' + self.name

