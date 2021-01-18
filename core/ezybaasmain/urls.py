"""ezybaasmain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from ezybaas import config
# from app_noauth import urls
# from app_basicauth import urls
# from app_sessionauth import urls
# from app_tokenauth import urls
from ezybaas import urls
from . import views


EZYB_URL_PREFIX = 'ezybaas/'
# if not config.EZYBAAS_RELEASE_STANDALONE:
# 	EZYB_URL_PREFIX = 'ezybaas/'

urlpatterns = [
	path('', views.index, name='index'),
	path('admin/', admin.site.urls),
	#path(EZYB_URL_PREFIX, include('ezybaas.urls'), name = 'ezybaas')
	#HttpResponseRedirect(reverse("appname:urlname"))
	# path('app_noauth/',include('app_noauth.urls')),
	# path('app_basicauth/',include('app_basicauth.urls')),
	# path('app_sessionauth/',include('app_sessionauth.urls')),
	# path('app_tokenauth/',include('app_tokenauth.urls')),
	path(EZYB_URL_PREFIX, include('ezybaas.urls'), name = 'ezybaas')

]





























urlpatterns.append(path('ezybaas/api/demo/', include('demo.urls'), name='demo'))   # WARNING: Added by EzyBaas. Please Do Not Remove.
