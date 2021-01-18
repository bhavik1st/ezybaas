# Copyright (c) 2019 Ezybaas by Bhavik Shah.
# CTO @ Susthitsoft Technologies Private Limited.
# All rights reserved.
# Please see the LICENSE.txt included as part of this package.


from django.contrib import admin

# Register your models here.
from .models import MetaModel,App,Table,DbSettings,Config

admin.site.register(MetaModel)
admin.site.register(App)
admin.site.register(Table)
admin.site.register(Config)
admin.site.register(DbSettings)




