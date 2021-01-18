# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.

from django.urls import path
from . import views, api
from django.conf.urls import include
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

# For Model Viewsets
from rest_framework.routers import SimpleRouter
from django.contrib.auth import views as auth_views

swagger_view = get_swagger_view(title="EzyBaaS API")

urlpatterns = [
	path('', views.DashboardPageView.as_view(), name='loginpage'),
	path('apps/', views.AppsPageView.as_view(), name='apps'),
	path('home/', views.index, name='index'),
	path('dashboard/', views.index, name='dashboard'),
	path('authentication', views.authentication, name='authentication'),
	path('database', views.database, name='database'),
	path('db', views.DatabaseView.as_view(), name='db'),
	path('save_to_file', views.save_to_file, name='save_to_file'),
	path('database_append', views.database_append, name='database_append'),
	path('database_new_table', views.database_new_table, name='database_new_table'),
	path('wizard', views.wizard, name='wizard'),
	path('editwizard', views.edit_wizard, name='editwizard'),
	path('login/', views.LoginPageView.as_view(), name='login'),
	path('logout/', views.LogoutPageView.as_view(), name='logout'),
	path('profile/', views.ProfilePageView.as_view(), name='profile'),
	path('dbsettings/', views.DbSettingsPageView.as_view(), name='dbsettings'),
	path('importdata/', views.ImportData.as_view(), name='importdata'),
	path('about/', views.AboutPageView.as_view(), name='about'),
	path('sysinfo/', views.Sysinfo.as_view(), name='sysinfo'),
	path('apidocs/', swagger_view, name='swagger'),
	
	path('api/ezybaas/version/', api.VersionAPI.as_view()),
	path('api/ezybaas/status/', api.StatusAPI.as_view()),
	path('api/ezybaas/status/<str:appname>', api.StatusAPI.as_view()),
	path('api/ezybaas/settings/apps/schema/', api.ImportExportAPI.as_view()),
	path('api/ezybaas/delete/<appname>', api.DeleteAPI.as_view()),
	path('api/ezybaas/sysinfo/', api.MonitoringAPI.as_view()),
	path('api/ezybaas/dbactive/', api.DBactiveAPI.as_view()),
	path('api/ezybaas/golive/', api.apiLiveAPI.as_view()),
	path('api/ezybaas/migrateApp/', api.migrateApp.as_view()),	

]

router = SimpleRouter()

# Model Viewsets
router.register(r'api/ezybaas/tables', api.TableViewSet,'table')
router.register(r'api/ezybaas/apps', api.AppViewSet,'apps')
router.register(r'api/ezybaas/fields', api.FieldViewSet,'fields')
router.register(r'api/ezybaas/db', api.DbSettingsViewSet,'db')
router.register(r'api/ezybaas/config', api.ConfigViewSet,'config')

urlpatterns += router.urls
