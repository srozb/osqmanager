from django.contrib import admin
from osquery import models


class BussinessUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class EventQueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'interval', 'enabled']
    list_filter = ['enabled', 'tag']
    search_fields = ['name']


class ClientConfigTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_name']


class OsqueryClientAdmin(admin.ModelAdmin):
    list_display = ['hostname', 'node_key', 'uuid',
                    'bussiness_unit', 'registered_date']
    list_filter = ['bussiness_unit']
    search_fields = ['node_key', 'hostname', 'uuid', 'tag']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
# Register your models here.


admin.site.register(models.BussinessUnit, BussinessUnitAdmin)
admin.site.register(models.ClientConfigTemplate, ClientConfigTemplateAdmin)
admin.site.register(models.EventQuery, EventQueryAdmin)
admin.site.register(models.OsqueryClient, OsqueryClientAdmin)
admin.site.register(models.Tag, TagAdmin)
