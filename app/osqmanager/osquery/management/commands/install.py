from django.core.management.base import BaseCommand, CommandError
from osquery.models import BussinessUnit, ClientConfigTemplate, EventQuery, Tag
import binascii
import os


class Command(BaseCommand):
    help = 'Generates initial data'

    config = """{
    "host_identifier": "uuid",
    "schedule_splay_percent": 10
}   """

    inventory_query = "SELECT name,version,platform FROM os_version;"

    def _generate_secret(self):
        return binascii.b2a_hex(os.urandom(32)).decode('utf-8')

    def _GenerateBU(self):
        if not BussinessUnit.objects.count():
            BussinessUnit.objects.create(
                name='default', secret=self._generate_secret(),
                description='auto-created')
            self.stdout.write(self.style.SUCCESS(
                'Default bussiness unit created.'))
        else:
            self.stdout.write(self.style.ERROR(
                'Bussiness unit already exists.'))

    def _GenerateConfig(self):
        if not ClientConfigTemplate.objects.count():
            bu = BussinessUnit.objects.get(name='default')
            ClientConfigTemplate.objects.create(template_name='default',
                                                template_description='auto-created by install script',
                                                template_config=self.config,
                                                bussiness_unit=bu)
            self.stdout.write(self.style.SUCCESS(
                'Default config template created.'))
        else:
            self.stdout.write(self.style.ERROR(
                'Client config template already exists.'))

    def _GenerateInventoryQuery(self):
        if not EventQuery.objects.count():
            default_tag = Tag.objects.get_or_create(name='default')
            eq = EventQuery.objects.create(name='Inventory OS',
            description='auto-generated by install script',
            value=self.inventory_query,
            enabled=True,
            interval=600)
            eq.tag.add(default_tag[0])
            self.stdout.write(self.style.SUCCESS(
                'Inventory query created.'))
        else:
            self.stdout.write(self.style.ERROR(
        'Inventory query already exists.'))

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-bussiness-unit',
            action='store_true',
            dest='nobu',
            default=False,
            help="Don't create default business_unit",
        )
        parser.add_argument(
            '--no-client-config-template',
            action='store_true',
            dest='noconfig',
            default=False,
            help="Don't create default client config template",
        )
        parser.add_argument(
            '--no-inventory-query',
            action='store_true',
            dest='noinventory',
            default=False,
            help="Don't create inventory query",
        )

    def handle(self, *args, **options):
        if options['noconfig'] and options['nobu'] and options['noinventory']:
            self.stdout.write(self.style.ERROR(
                'Error: will not create anything...'))
        else:
            if not options['nobu']:
                self._GenerateBU()
            if not options['noconfig']:
                self._GenerateConfig()
            if not options['noinventory']:
                self._GenerateInventoryQuery()
            self.stdout.write(self.style.SUCCESS(
                'All done. Remember to create superuser.'))
