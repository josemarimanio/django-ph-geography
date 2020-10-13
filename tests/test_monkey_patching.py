import os

from django_migration_testcase import MigrationTest

from django.conf import settings
from django.core import management
from django.core.exceptions import FieldDoesNotExist
from django.db import models

from ph_geography.models import PhilippineGeography
from ph_geography.models import Barangay
from ph_geography.models import Municipality
from ph_geography.models import Province
from ph_geography.models import Region


class MonkeyPatchingTestCase(MigrationTest):
    """
    Test cases for django-ph-geography monkey patching

    Testing these test cases:
        * Adding field to a specific model
        * Adding field to all models (via abstract model)
        * Removing field to a specific model
        * Removing field to all models (via abstract model)
    """
    app_name = 'ph_geography'
    apps_after = None
    before = '0001'
    after = '0002'

    ADDED_FIELD_SPECIFIC = 'specific'
    ADDED_FIELD_ALL = 'all'
    REMOVED_FIELD_SPECIFIC = 'is_urban'
    REMOVED_FIELD_ALL = 'population'
    MIGRATION_FILE_NAME = 'monkey_patching'

    @classmethod
    def setUpClass(cls):
        """Apply monkey patching to the provided models and generate a temporary migration file"""
        super(MonkeyPatchingTestCase, cls).setUpClass()

        # Add field to specific model
        Barangay.add_field(cls.ADDED_FIELD_SPECIFIC, models.BooleanField(default=True))

        # Add field to all models
        PhilippineGeography.add_field(cls.ADDED_FIELD_ALL, models.BooleanField(default=True))

        # Remove field to specific model
        Barangay.remove_field(cls.REMOVED_FIELD_SPECIFIC)

        # Remove field to all models
        PhilippineGeography.remove_field(cls.REMOVED_FIELD_ALL)

        # Remove field 'name' to test __str__ output
        Region.remove_field('name')

        # Remove field 'name' to test __repr__ 1st fallback output
        Province.remove_field('code')

        # Remove field 'name' and 'code' to test __repr__ 2nd fallback output
        Municipality.remove_field('code', 'name')

        management.call_command('makemigrations', 'ph_geography',
                                name=cls.MIGRATION_FILE_NAME, verbosity=0, interactive=False)

    @classmethod
    def tearDownClass(cls):
        """Delete generated migration file after completing testing"""
        path = os.path.join(*[
            settings.BASE_DIR,
            'ph_geography',
            'migrations',
            '{}_{}.py'.format(cls.after, cls.MIGRATION_FILE_NAME),
        ])
        if os.path.isfile(path):
            os.remove(path)
        super(MonkeyPatchingTestCase, cls).tearDownClass()

    def setUp(self):
        """Run migration file and refresh models to reflect the changes"""
        super(MonkeyPatchingTestCase, self).setUp()
        self.run_migration()
        self.barangay_model = self.get_model_after('Barangay')
        self.municipality_model = self.get_model_after('Municipality')
        self.province_model = self.get_model_after('Province')
        self.region_model = self.get_model_after('Region')

    #
    #   __str__ and __repr__
    #
    def test_remove_field_name_str(self):
        region = Region.objects.create(pk=1, code='REGION', island_group=Region.ISLAND_GROUP_LUZON)
        self.assertTrue(str(region))

    def test_remove_field_code_repr(self):
        region = Region.objects.create(code='REGION', island_group=Region.ISLAND_GROUP_LUZON)
        province = Province.objects.create(name='PROVINCE', region=region)
        self.assertTrue(repr(province))

    def test_remove_field_code_name_repr(self):
        region = Region.objects.create(code='REGION', island_group=Region.ISLAND_GROUP_LUZON)
        province = Province.objects.create(name='PROVINCE', region=region)
        municipality = Municipality.objects.create(pk=1, province=province, is_city=False, is_capital=False)
        self.assertTrue(repr(municipality))

    #
    #   Remove field
    #
    def test_remove_field_specific_model_result(self):
        with self.assertRaises(FieldDoesNotExist):
            self.barangay_model._meta.get_field(self.REMOVED_FIELD_SPECIFIC)

    def test_remove_field_all_models_result(self):
        removed = []
        try:
            self.barangay_model._meta.get_field(self.REMOVED_FIELD_ALL)
            removed.append(False)
        except FieldDoesNotExist:
            removed.append(True)
        try:
            self.municipality_model._meta.get_field(self.REMOVED_FIELD_ALL)
            removed.append(False)
        except FieldDoesNotExist:
            removed.append(True)
        try:
            self.province_model._meta.get_field(self.REMOVED_FIELD_ALL)
            removed.append(False)
        except FieldDoesNotExist:
            removed.append(True)
        try:
            self.region_model._meta.get_field(self.REMOVED_FIELD_ALL)
            removed.append(False)
        except FieldDoesNotExist:
            removed.append(True)
        self.assertTrue(all(removed))

    def test_remove_field_specific_model_params_not_str(self):
        with self.assertRaises(TypeError):
            Barangay.remove_field('code', 123)

    def test_remove_field_all_models_params_not_str(self):
        with self.assertRaises(TypeError):
            PhilippineGeography.remove_field('code', 123)

    def test_remove_field_specific_model_not_found(self):
        with self.assertRaises(AttributeError):
            Barangay.remove_field('_')

    def test_remove_field_all_models_not_found(self):
        with self.assertRaises(AttributeError):
            PhilippineGeography.remove_field('_')

    #
    #   Add field
    #
    def test_add_field_specific_model_result(self):
        self.assertTrue(self.barangay_model._meta.get_field(self.ADDED_FIELD_SPECIFIC))

    def test_add_field_all_models_result(self):
        added = []
        try:
            self.barangay_model._meta.get_field(self.ADDED_FIELD_ALL)
            added.append(True)
        except FieldDoesNotExist:
            added.append(False)
        try:
            self.municipality_model._meta.get_field(self.ADDED_FIELD_ALL)
            added.append(True)
        except FieldDoesNotExist:
            added.append(False)
        try:
            self.province_model._meta.get_field(self.ADDED_FIELD_ALL)
            added.append(True)
        except FieldDoesNotExist:
            added.append(False)
        try:
            self.region_model._meta.get_field(self.ADDED_FIELD_ALL)
            added.append(True)
        except FieldDoesNotExist:
            added.append(False)
        self.assertTrue(all(added))
