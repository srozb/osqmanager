from __future__ import unicode_literals

from django.db import models


class BussinessUnit(models.Model):
    name = models.CharField(
        max_length=128, help_text="Provide bussiness unit's name")
    secret = models.TextField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'bussiness_unit'

    def __str__(self):
        return "{}".format(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return "{}".format(self.name)


class ClientConfigTemplate(models.Model):
    default_config = """{
    "host_identifier": "uuid",
    "schedule_splay_percent": 10
}"""

    template_name = models.CharField(max_length=512, unique=True)
    template_description = models.TextField(blank=True)
    template_config = models.TextField(default=default_config)
    bussiness_unit = models.OneToOneField(BussinessUnit, help_text="Assigned bussiness unit")

    class Meta:
        db_table = 'client_config'

    def __str__(self):
        return "{}".format(self.template_name)


class EventQuery(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    value = models.TextField(help_text="OSQ query itself")
    enabled = models.BooleanField(default=False)
    interval = models.IntegerField(default=3600)
    tag = models.ManyToManyField(Tag, blank=True)

    class Meta:
        db_table = 'event_query'
        verbose_name = "Event query"
        verbose_name_plural = "Event queries"

    def __str__(self):
        return "{}".format(self.name)


class OsqueryClient(models.Model):
    node_key = models.CharField(max_length=1024, unique=True)
    hostname = models.CharField(max_length=512, blank=True)
    uuid = models.UUIDField(blank=True, unique=True)
    bussiness_unit = models.ForeignKey(BussinessUnit)
    registered_date = models.DateTimeField(blank=True)
    ip = models.GenericIPAddressField()
    version = models.CharField(max_length=512)
    tag = models.ManyToManyField(Tag, help_text="Client tags", blank=True)
    last_distributed_id = models.IntegerField(default=0)

    class Meta:
        db_table = 'osquery_client'

    def __str__(self):
        return "{}".format(self.hostname)

class DistributedQuery(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    value = models.TextField(help_text="OSQ query itself")
    enabled = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag, blank=True)

    class Meta:
        db_table = 'distributed_query'
        verbose_name = "Distributed query"
        verbose_name_plural = "Distributed queries"

    def __str__(self):
        return "{}".format(self.name)
