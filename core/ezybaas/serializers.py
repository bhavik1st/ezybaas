# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.

from rest_framework import serializers
from .models import MetaModel, App, Table, Config, DbSettings

class VersionSerializer(serializers.Serializer):
		name = serializers.CharField()
		author = serializers.CharField()
		version = serializers.CharField() 
		releasenotes = serializers.CharField() 
		releasedate = serializers.DateField()
		standalone = serializers.BooleanField()
		license = serializers.CharField()
		now = serializers.DateTimeField()

class DbSettingsSerializer(serializers.ModelSerializer):

	class Meta:
		model = DbSettings
#		extra_kwargs = {'password': {'write_only': True}, 'created': {'read_only': True}, 'modified': {'read_only': True}}
		fields = ('key', 'type','name','host','port','user','password','atomic','commit','active')
		
class ConfigSerializer(serializers.ModelSerializer):

	class Meta:
		model = Config
		fields = ('key','value')
		
class AppSerializer(serializers.ModelSerializer):
	class Meta:
		model = App
		fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Table
		fields = '__all__'
		
class MetaModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = MetaModel
		fields = '__all__'









		

		