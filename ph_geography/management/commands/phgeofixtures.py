from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load all PH Geography fixtures.'

    def __init__(self):
        super(Command, self).__init__()
        self.app_name = 'ph_geography'
        self.region_fixtures = 'regions.json'
        self.province_fixtures = 'provinces.json'
        self.municipality_fixtures = 'municipalities.json'
        self.barangay_fixtures = 'barangays.json'

    def handle(self, *args, **kwargs):
        management.call_command('loaddata', self.region_fixtures, app=self.app_name)
        management.call_command('loaddata', self.province_fixtures, app=self.app_name)
        management.call_command('loaddata', self.municipality_fixtures, app=self.app_name)
        management.call_command('loaddata', self.barangay_fixtures, app=self.app_name)
