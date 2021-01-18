# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.


# from django.test import TestCase
import os
import shutil
from .models import MetaModel
from .baas import create_app
from ezybaas import baas
# Create your tests here.

# app = "myApp4"
app = 'testapp4'
class MetaModelTestCase(TestCase):
	
	# @classmethod
	# def setUpClass(cls):
	# 	super().setUpClass()
	# 	os.path.

	# @classmethod
	# def tearDownClass(cls):
	# 	#...
	# 	#MetaModel.objects.delete()
	# 	#MetaModel.objects.get(App="myApp").delete()
	# 	direc = os.path.dirname(__file__)
	# 	file_path = os.path.abspath(os.path.join(direc, '..' , app))
	# 	shutil.rmtree(file_path)
	# 	super().tearDownClass()
	
	# def test_app(self):
	# 	create_app(app=app)
	# 	direc = os.path.dirname(__file__)
	# 	file_path = os.path.abspath(os.path.join(direc, '..' , app))
		
	# 	appfolderthere = os.path.exists(file_path)
	# 	# myApp = MetaModel.objects.get(App="app")
	# 	self.assertTrue(appfolderthere)

	def test_create_api(self):
		baas.create_api(app)
		direc = os.path.dirname(__file__)
		file_path = os.path.abspath(os.path.join(direc, app, 'api.py'))
		self.assertTrue(file_path)

	def test_create_urls(self):
		baas.create_url(app)
		direc = os.path.dirname(__file__)
		file_path = os.path.abspath(os.path.join(direc, app, 'urls.py'))
		self.assertTrue(file_path)


