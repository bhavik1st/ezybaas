# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.

from . import config
from . import constants
from . import utils
from . import baas
from .models import MetaModel, App, DbSettings, Config, Table, Version
from .serializers import MetaModelSerializer, AppSerializer

from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.contrib import messages # Messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core import management

# Auth
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

# For checking user permission
from django.contrib.auth.mixins import UserPassesTestMixin

from django.views.generic import (ListView, TemplateView, View)
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import (redirect, render)
from django.utils.translation import gettext as _
from django.urls import reverse


# ASPER: https://stackoverflow.com/questions/12003736/django-login-required-decorator-for-a-superuser
# ASPER: https://docs.djangoproject.com/en/dev/topics/auth/default/#django.contrib.auth.decorators.user_passes_test
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.mixins import UserPassesTestMixin

import requests
from .api import *



class IsSuperUserMixin(UserPassesTestMixin):
	def test_func(self):
		return self.request.user.is_superuser

class AppsPageView(IsSuperUserMixin, TemplateView):
	template_name = 'ezybaas/apps.html'
	
	def get_context_data(self, **kwargs):
		context = get_dashboard_context(self.request)
		return context

'''
	def get(self, request, **kwargs):
		try:
			context = get_dashboard_context()
			return render(request, 'ezybaas/apps.html', context={'login_error': error})
			
		except Exception as e:
			error = _("Error occurred! Cause: ") + e.__cause__
			messages.add_message(request, messages.ERROR, error)

		return render(request, 'ezybaas/login.html', context={'login_error': error })
'''
# Create your views here.
class DashboardPageView(IsSuperUserMixin, TemplateView):
	template_name = 'ezybaas/index.html'
	
	def get(self, request, **kwargs):
		try:
			if request.user and request.user.is_superuser:
				return index(request)
			else:
				return render(request, 'ezybaas/login.html',context={'login_error': None})
			pass
		except Exception as e:
			error = ("Error occurred! Cause: ") + str(e.__cause__)
		
			error="error"
			messages.add_message(request, messages.ERROR, error)

		return render(request, 'ezybaas/login.html')

class LoginPageView(TemplateView):
	template_name = 'ezybaas/login.html'

	def get(self, request, **kwargs):
		return render(request, 'ezybaas/login.html', context={'login_error': None})

	def post(self, request, **kwargs):
		error = None
		username = request.POST['username'] #request.POST.get("title", "")
		password = request.POST['password']
		next = "index"
		user = authenticate(request, username=username, password=password)
		try:
			if user is not None:
				# the password verified for the user
				if user.is_active:
					if user.is_superuser:
						login(request, user)
						if next:
							return redirect(next)
						return index(request)  # return render(request, 'home.html', context={'app': AppConfig, 'error': False })
					else:
						logout(request)
						error = _(constants.MSG_USER_NOT_SUPERUSER)
				else:
					logout(request)
					error = _(constants.MSG_USER_INACTIVE)

			else:
				error = _(constants.MSG_USER_PWD_INVALID)
		except Exception as e:
			error = _("Error occurred! Cause: ") + e.__cause__
		
		messages.add_message(request, messages.ERROR, error)
		return render(request, 'ezybaas/login.html', context={'login_error': error })



class LogoutPageView(TemplateView):
	template_name = 'ezybaas/logout.html'

	def get(self, request, **kwargs):
		logout(request)
		warning = _(constants.MSG_USER_LOGOUT)

		messages.add_message(request, messages.INFO, warning)
		return render(request, 'ezybaas/login.html', context={'login_error': warning} )


# ASPER - https://stackoverflow.com/questions/1873806/how-to-allow-users-to-change-their-own-passwords-in-django
class ProfilePageView(IsSuperUserMixin, TemplateView):
	template_name = 'ezybaas/profile.html'

	def get(self, request, **kwargs):
		context = get_database_context(request)
		return render(request, 'ezybaas/profile.html', context)

	def post(self, request, **kwargs):
		old_pass = request.POST.get('input-old-password','')
		new_pass = request.POST.get('input-new-password','')
		new_pass_again = request.POST.get('input-new-password-again', '')
		

		try:
			if not request.user.check_password(old_pass):
				messages.add_message(request, messages.ERROR, constants.MSG_PWD_OLD_INVALID)
			elif new_pass != new_pass_again:
				messages.add_message(request, messages.ERROR, constants.MSG_PWD_NOT_MATCHING)
			else:
				request.user.set_password(new_pass)
				request.user.save()
				update_session_auth_hash(request, request.user)
				messages.add_message(request, messages.INFO, constants.MSG_PWD_CHANGED)

		except Exception as e:
			print('Exception ' + str(e))
			pass

		return render(request, 'ezybaas/profile.html')


class DbSettingsPageView(IsSuperUserMixin, TemplateView):
	template_name = 'ezybaas/dbsettings.html'

	def get(self, request, **kwargs):
		context = get_dashboard_context(request)
		return render(request, 'ezybaas/dbsettings.html', context)


	def post(self, request, **kwargs):
		old_pass = request.POST.get('input-old-password','')
		new_pass = request.POST.get('input-new-password','')
		new_pass_again = request.POST.get('input-new-password-again','')

		try:
			if not request.user.check_password(old_pass):
				messages.add_message(request, messages.ERROR, constants.MSG_PWD_OLD_INVALID)
			elif new_pass != new_pass_again:
				messages.add_message(request, messages.ERROR, constants.MSG_PWD_NOT_MATCHING)
			else:
				request.user.set_password(new_pass)
				request.user.save()
				update_session_auth_hash(request, request.user)
				messages.add_message(request, messages.INFO, constants.MSG_PWD_CHANGED)

		except Exception as e:
			print('Exception ' + str(e))
			pass

		return render(request, 'ezybaas/profile.html')




@user_passes_test(lambda u: u.is_superuser)
def erd(request):
	context = get_dashboard_context(request)	
	return render(request, 'ezybaas/erd.html', context)

@user_passes_test(lambda u: u.is_superuser)
def index(request):
	context = get_dashboard_context(request)	
	return render(request, 'ezybaas/index.html', context)

def wizard(request):
	context = get_dashboard_context(request)	
	return render(request, 'ezybaas/wizard.html', context)

def edit_wizard(request):
	app = request.GET['app']
	context = get_dashboard_context(request)
	return render(request, 'ezybaas/editWizard.html', context, app)

def get_dashboard_context(request):
	apps = utils.get_apps()
	models = []
	if request.method == 'GET' and 'app' in request.GET:
		models = utils.get_models(request.GET['app'])
	# else:
	#	 models = utils.get_models(apps[0])

	tables = utils.get_tables()
	fields = MetaModel.objects.filter().values()

	context = {
			'apps' : apps, 
			'models' : models, 
			'app_count' : len(apps),
			'table_count' : len(tables),
			'fields_count' : len(fields),
			'app_data' : utils.populate_index_table(),
	 		'mode': config.EZYBAAS_RELEASE_STANDALONE,
			'version': Version(),
			'ezybaas_version':config.EZYBAAS_RELEASE_VERSION,
			}
	return context

def authentication(request):
	context = get_dashboard_context(request)
	return render(request, 'ezybaas/authentication.html', context)

def database(request):
	fields = []
	tables = []
	if request.method == 'GET' and 'app' in request.GET:
		fields = utils.get_fields(request.GET['app'])
		tables = utils.get_tables(request.GET['app'])
	else:
		fields =[]
		tables = []
	
	context = {'apps':utils.get_apps(), 'tables':tables, 'fields' : fields, 'data' : get_dashboard_context(request)}
	return render(request, 'ezybaas/database.html',context)

def get_database_context(request):
	fields = []
	tables = []
	if request.method == 'GET' and 'app' in request.GET:
		fields = utils.get_fields(request.GET['app'])
		tables = utils.get_tables(request.GET['app'])
	else:
		fields =[]
		tables = []

	context = {'apps':utils.get_apps(), 'tables':tables, 'fields' : fields, 'context' : get_dashboard_context(request)}
	return context

class DatabaseView(TemplateView):
	template_name = 'ezybaas/database.html'

	def get_context_data(self, *args, **kwargs):
		context = get_database_context(self.request)
		return context


def database_append(request):
	if request.method == 'POST':
		print('\n\n')
		print(request.POST['app'])
		print(request.POST['table'])
		print(request.POST['tblAppendGrid_rowOrder'])
		print('printed')
		my_list = request.POST['tblAppendGrid_rowOrder'].split(",")
		n = len(my_list)

		baas.append_function(request.POST['app'],request.POST['table'],request,len(my_list))
		baas.create_models(request.POST['app'])	

	return render(request, 'ezybaas/index.html',)

def database_new_table(request):
	context = {}

	if request.method == 'GET' and 'app' in request.GET:
		app = request.GET["app"]
		context = { 'app' : app}
		print("APPPPP\n\n" + str(context))

	return render(request, 'ezybaas/database_new_table.html',context)

def save_to_file(request):
	if request.method == 'GET' and 'app' in request.GET:
		app = request.GET['app']
		fields = utils.get_fields(app)
		tables = utils.get_tables(app)
		baas.go_live(app)
	else:
		fields =[]
		tables = []
	context = {'apps':utils.get_apps(), 'tables':tables, 'fields' : fields}
	return index(context)


class ImportData(TemplateView):
	template_name = 'ezybaas/import.html'

	def get_context_data(self, *args, **kwargs):
		context = get_dashboard_context(self.request)
		return context


class Sysinfo(TemplateView):
	template_name = 'ezybaas/sysinfo.html'

	def get_context_data(self, *args, **kwargs):
		context = get_dashboard_context(self.request)
		return context

class AboutPageView(TemplateView):
	template_name = 'ezybaas/about.html'

	def get_context_data(self, *args, **kwargs):
		context = get_dashboard_context(self.request)
		return context

class LayoutPageView(TemplateView):
	template_name = 'ezybaas/layout.html'

	def get_context_data(self, *args, **kwargs):
		context = get_dashboard_context(self.request)
		return context

