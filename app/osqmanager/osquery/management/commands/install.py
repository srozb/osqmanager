from django.core.management.base import BaseCommand, CommandError
from osquery.models import BussinessUnit, ClientConfigTemplate
import binascii
import os


class Command(BaseCommand):
    help = 'Generates initial data'

    config = """{
    "host_identifier": "uuid",
    "schedule_splay_percent": 10
}   """

    def _generate_secret(self):
        return binascii.b2a_hex(os.urandom(32)).decode('utf-8')

    def _GenerateBU(self):
        if not BussinessUnit.objects.count():
            BussinessUnit.objects.create(
                name='default', secret=self._generate_secret(),
                description='auto-created')
            self.stdout.write(self.style.SUCCESS(
                'Default bussiness unit saved into the DB.'))
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
                'Default config template saved into the DB.'))
        else:
            self.stdout.write(self.style.ERROR(
                'Client config template already exists.'))

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

    def handle(self, *args, **options):
        if options['noconfig'] and options['nobu']:
            self.stdout.write(self.style.ERROR(
                'Error: will not create anything...'))
        else:
            if not options['nobu']:
                self._GenerateBU()
            if not options['noconfig']:
                self._GenerateConfig()
            self.stdout.write(self.style.SUCCESS(
                'All done. Remember to create superuser.'))
