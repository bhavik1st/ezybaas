# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.

from . import constants
from jinja2 import Environment, FileSystemLoader
from . import config
import os
from datetime import datetime
''' 

from ezybaas.generator import CodeGenerator
cg = CodeGenerator()
cg.get_temp('code/sumprices.txt')
cg.genModelFile('temp','temp')

'''

class CodeGenerator:

	def __init__(self, template_folder = None):
		default_template_folder = os.path.abspath(os.path.join(config.BAAS_NAME,constants.CODE_TEMPLATE_FOLDER))
		
		if template_folder == None:
			template_folder = [ default_template_folder ]
		else:
		 	template_folder = [default_template_folder, template_folder]
			  
		self.template_folder = template_folder
		self.file_loader = FileSystemLoader(self.template_folder)
		self.env = Environment(loader=self.file_loader, trim_blocks=True)
		
		#def_env = Environment(loader=file_loader)

	def get_temp(self, template):
		cars = [
			{'name': 'Audi', 'price': 23000}, 
			{'name': 'Skoda', 'price': 17300}, 
			{'name': 'Volvo', 'price': 44300}, 
			{'name': 'Volkswagen', 'price': 21300}
		]

		template = self.env.get_template(template)

		output = template.render(cars=cars)
		print(output)
		return os.path.abspath(config.BAAS_NAME)

	def get_environment(self):
		cars = [
			{'name': 'Audi', 'price': 23000}, 
			{'name': 'Skoda', 'price': 17300}, 
			{'name': 'Volvo', 'price': 44300}, 
			{'name': 'Volkswagen', 'price': 21300}
		]

		template = self.env.get_template('sumprices.txt')

		output = template.render(cars=cars)
		print(output)

	def genModelFile(self, output_folder, output_file):
		models = [
			{
				'name': 'Cars',
				'fields': [
					{'name': 'Audi', 'type': 'CharField'}, 
					{'name': 'Skoda', 'type': 'IntField'}
				]
			},
			{
				'name': 'Planes',
				'fields': [
					{'name': 'Boeing', 'type': 'BooleanField'}, 
					{'name': 'Airbus', 'type': 'CharField'}
				]
			}
		]

		template = self.env.get_template('code/models.txt')

		output = template.render(models = models, date = datetime.utcnow()  )
		print(output)
		pass

	pass