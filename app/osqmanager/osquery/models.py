from __future__ import unicode_literals

from django.db import models
from osqmanager import settings
from datetime import datetime, timedelta, tzinfo
from django.utils import timezone


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


class TagAssignmentRules(models.Model):
    RULE_TYPES = (
        ('IP', 'Single IP address'),
        ('SUBNET', 'IP subnet CIDR'),
        ('REGEX', 'Host identifier regex')
    )
    tag = models.ForeignKey(Tag)
    type = models.CharField(max_length=8, choices=RULE_TYPES, default='SUBNET')
    value = models.CharField(max_length=256, unique=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=False)


class ClientConfigTemplate(models.Model):
    default_config = """{
    "host_identifier": "uuid",
    "schedule_splay_percent": 10
}"""

    template_name = models.CharField(max_length=512, unique=True)
    template_description = models.TextField(blank=True)
    template_config = models.TextField(default=default_config)
    bussiness_unit = models.OneToOneField(
        BussinessUnit, help_text="Assigned bussiness unit")

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
    uuid = models.UUIDField(blank=True, null=True, unique=True)
    bussiness_unit = models.ForeignKey(BussinessUnit)
    registered_date = models.DateTimeField(blank=True)
    last_communication = models.DateTimeField(blank=True)
    ip = models.GenericIPAddressField()
    version = models.CharField(max_length=512)
    platform = models.CharField(max_length=512, blank=True, null=True)
    os_name = models.CharField(max_length=512, blank=True, null=True)
    os_version = models.CharField(max_length=256, blank=True, null=True)
    tag = models.ManyToManyField(Tag, help_text="Client tags", blank=True)
    last_distributed_id = models.IntegerField(default=0)

    def is_alive(self):
        boolean = True
        time_diff = timezone.now() - self.last_communication
        return time_diff.total_seconds() < 600  # TODO: move hardcoded to settin

    is_alive.boolean = True

    def __str__(self):
        return "{}".format(self.hostname)

    class Meta:
        db_table = 'osquery_client'


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
