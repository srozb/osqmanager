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
                    'bussiness_unit', 'registered_date', 'last_communication',
                    'ip', 'version', 'is_alive']
    list_filter = ['bussiness_unit', 'version']
    search_fields = ['node_key', 'hostname', 'uuid', 'tag', 'ip']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class TagAssignmentRulesAdmin(admin.ModelAdmin):
    list_display = ['tag', 'type', 'value', 'description', 'enabled']
    list_filter = ['enabled', 'tag', 'type']
    search_fields = ['value', 'description']


class DistributedQueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'enabled']
    list_filter = ['enabled', 'tag']
    search_fields = ['name']


admin.site.register(models.BussinessUnit, BussinessUnitAdmin)
admin.site.register(models.ClientConfigTemplate, ClientConfigTemplateAdmin)
admin.site.register(models.EventQuery, EventQueryAdmin)
admin.site.register(models.OsqueryClient, OsqueryClientAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.TagAssignmentRules, TagAssignmentRulesAdmin)
admin.site.register(models.DistributedQuery, DistributedQueryAdmin)
