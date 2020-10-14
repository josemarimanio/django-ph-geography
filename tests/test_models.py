from django.test import TestCase

from ph_geography.models import Barangay
from ph_geography.models import Municipality
from ph_geography.models import Province
from ph_geography.models import Region


class ModelTestCase(TestCase):
    """
    Test cases for django-ph-geography models

    Testing theses cases:
        * __str__() and __repr() implementation
        * Model field list
        * CharField choices
        * ForeignKey related_name
        * Model properties
    """
    fixtures = ('geography.json',)

    BARANGAY_NAME = 'DOÑA IMELDA'
    MUNICIPALITY_NAME = 'QUEZON CITY'
    PROVINCE_NAME = 'METRO MANILA'
    REGION_NAME = 'NATIONAL CAPITAL REGION (NCR)'

    @staticmethod
    def get_sorted_field_names(model):
        """Returns a sorted list of field names"""
        return sorted([field.name for field in model._meta.get_fields()])

    @staticmethod
    def repr_output(item):
        """Returns a string of simulated model __repr__ response"""
        return '<Code: {code}, {model}: {name}>'.format(
            code=getattr(item, 'code'),
            model=item.__class__.__name__,
            name=getattr(item, 'name'),
        )

    def setUp(self):
        self.barangay = Barangay.objects.get(name=self.BARANGAY_NAME)
        self.municipality = Municipality.objects.get(name=self.MUNICIPALITY_NAME)
        self.province = Province.objects.get(name=self.PROVINCE_NAME)
        self.region = Region.objects.get(name=self.REGION_NAME)

    #
    #   Region
    #
    def test_region_str(self):
        self.assertEqual(str(self.region), self.REGION_NAME)

    def test_region_repr(self):
        self.assertEqual(
            repr(self.region),
            self.repr_output(self.region)
        )

    def test_region_fields_list(self):
        self.assertEqual(
            self.get_sorted_field_names(Region),
            ['code', 'id', 'is_active', 'island_group', 'name', 'population', 'province']
        )

    def test_region_island_group_choices(self):
        self.assertEqual(
            Region.ISLAND_GROUP_CHOICES,
            (('L', 'LUZON'), ('V', 'VISAYAS'), ('M', 'MINDANAO'))
        )

    def test_region_provinces(self):
        self.assertTrue(self.region.provinces.all().count())

    #
    #   Province
    #
    def test_province_str(self):
        self.assertEqual(str(self.province), self.PROVINCE_NAME)

    def test_province_repr(self):
        self.assertEqual(repr(self.province), self.repr_output(self.province))

    def test_province_fields_list(self):
        self.assertEqual(
            self.get_sorted_field_names(Province),
            ['code', 'id', 'income_class', 'is_active', 'municipality', 'name', 'population', 'region', ]
        )

    def test_province_income_class_choices(self):
        self.assertEqual(
            Province.INCOME_CLASS_CHOICES,
            (('1', '1ST'), ('2', '2ND'), ('3', '3RD'), ('4', '4TH'), ('5', '5TH'), ('6', '6TH'), ('S', 'SPECIAL'))
        )

    def test_province_municipalities(self):
        self.assertTrue(self.province.municipalities.all().count())

    def test_province_island_group(self):
        self.assertEqual(self.province.island_group, self.region.island_group)

    #
    #   Municipality
    #
    def test_municipality_str(self):
        self.assertEqual(str(self.municipality), self.MUNICIPALITY_NAME)

    def test_municipality_repr(self):
        self.assertEqual(repr(self.municipality), self.repr_output(self.municipality))

    def test_municipality_fields_list(self):
        self.assertEqual(
            self.get_sorted_field_names(Municipality),
            ['barangays', 'city_class', 'code', 'id', 'income_class', 'is_active',
             'is_capital', 'is_city', 'name', 'population', 'province', ]
        )

    def test_municipality_city_class_choices(self):
        self.assertEqual(
            Municipality.CITY_CLASS_CHOICES,
            (('C', 'CC'), ('I', 'ICC'), ('H', 'HUC'))
        )

    def test_municipality_income_class_choices(self):
        self.assertEqual(
            Municipality.INCOME_CLASS_CHOICES,
            (('1', '1ST'), ('2', '2ND'), ('3', '3RD'), ('4', '4TH'), ('5', '5TH'), ('6', '6TH'), ('S', 'SPECIAL'))
        )

    def test_municipality_barangays(self):
        self.assertTrue(self.municipality.barangays.all().count())

    def test_municipality_region(self):
        self.assertEqual(self.municipality.region, self.region)

    def test_municipality_island_group(self):
        self.assertEqual(self.municipality.island_group, Region.ISLAND_GROUP_LUZON)

    #
    #   Barangay
    #
    def test_barangay_str(self):
        self.assertEqual(str(self.barangay), self.BARANGAY_NAME)

    def test_barangay_repr(self):
        self.assertEqual(repr(self.barangay), self.repr_output(self.barangay))

    def test_barangay_fields_list(self):
        self.assertEqual(
            self.get_sorted_field_names(Barangay),
            ['code', 'id', 'is_active', 'is_urban', 'municipality', 'name', 'population']
        )

    def test_barangay_province(self):
        self.assertEqual(self.barangay.province, self.province)

    def test_barangay_region(self):
        self.assertEqual(self.barangay.region, self.region)

    def test_barangay_island_group(self):
        self.assertEqual(self.barangay.island_group, self.region.island_group)
