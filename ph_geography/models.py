from django.core.exceptions import FieldDoesNotExist
from django.db import models


class PhilippineGeography(models.Model):
    """
    Abstract model for common geographical fields.

    (Also a Yoyoy Villame song: https://www.youtube.com/watch?v=e_PMcFjE9as)

    Available fields are:
        * code - Unique geographical code.
        * name - Geographical name.
        * population - Population count based on 2015 POPCEN.
                        Null value  means no data is available.
        * is_active - Toggle if entry is active (True) or not (False).
    """
    code = models.CharField(max_length=10, unique=True, null=False, verbose_name='Code')
    name = models.CharField(max_length=100, null=False, verbose_name='Name')
    population = models.PositiveIntegerField(null=True, verbose_name='Population')
    is_active = models.BooleanField(null=False, default=True, verbose_name='Is Active')

    class Meta:
        abstract = True

    @classmethod
    def add_field(cls, name, value):
        """
        Add a field to the model.

        Using this method to the abstract model will apply the action to all subclasses.
        """
        if cls._meta.abstract:
            for subcls in cls.__subclasses__():
                subcls.add_to_class(name, value)
        else:
            cls.add_to_class(name, value)

    @classmethod
    def _remove_field(cls, names):
        """
        Remove fields from the model.
        """
        for name in names:
            try:
                field = cls._meta.get_field(name)
            except FieldDoesNotExist:
                raise AttributeError('No attribute name found in model: {name}'.format(name=name))
            else:
                cls._meta.local_fields.remove(field)

    @classmethod
    def remove_field(cls, *names):
        """
        Remove fields from the model.

        Supports *args of <str> field names.

        Using this method to the abstract model will apply the action to all subclasses.
        """

        if not all(isinstance(name, str) for name in names):
            raise TypeError('"remove_field" only supports <str> of field names.')

        if cls._meta.abstract:
            is_removed = False
            for subcls in cls.__subclasses__():
                try:
                    subcls._remove_field(names)
                except AttributeError:
                    pass
                else:
                    is_removed = True
            if not is_removed:
                raise AttributeError('No attribute name found in any model: {names}'.format(names=', '.join(names)))
        else:
            cls._remove_field(names)

    def __repr__(self):
        code = getattr(self, 'code', None)
        name = getattr(self, 'name', None)
        model = self.__class__.__name__
        if code and name:
            value = '<Code: {code}, {model}: {name}>'.format(code=code, model=model, name=name)
        elif name:
            value = '<{model}: {name}>'.format(model=model, name=name)
        else:
            value = super(PhilippineGeography, self).__repr__()
        return value

    def __str__(self):
        return getattr(self, 'name', None) or super(PhilippineGeography, self).__str__()


class Region(PhilippineGeography):
    """
    Model for regions.

    Available fields are:
        * code - Unique geographical code for region.
        * name - Geographical name for region.
        * population - Population count based on 2015 POPCEN.
                        Null value means no data is available.
        * island_group - Island group where the region is located. Possible values are 'L' (for Luzon),
                         'V' (for Visayas), and 'M' (for Mindanao).
        * is_active - Toggle if region is active (True) or not (False).
    """
    ISLAND_GROUP_LUZON = 'L'
    ISLAND_GROUP_VISAYAS = 'V'
    ISLAND_GROUP_MINDANAO = 'M'
    ISLAND_GROUP_CHOICES = (
        (ISLAND_GROUP_LUZON, 'LUZON'),
        (ISLAND_GROUP_VISAYAS, 'VISAYAS'),
        (ISLAND_GROUP_MINDANAO, 'MINDANAO'),
    )

    island_group = models.CharField(max_length=1, choices=ISLAND_GROUP_CHOICES,
                                    null=False, verbose_name='Island Group')

    class Meta:
        db_table = 'ph_geography_region'
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'


class Province(PhilippineGeography):
    """
    Model for provinces.

    Available fields are:
        * code - Unique geographical code for province.
        * name - Geographical name for province.
        * population - Population count based on 2015 POPCEN.
                        Null value means no data is available.
        * region - Region where the province is located.
        * income_class - Income classification. Possible values are '1' (1st), '2' (2nd), '3' (3rd),
                          '4' (4th), '5' (5th), '6' (6th), and 'S' (Special).
                          Blank means no data is available.
        * is_active - Toggle if province is active (True) or not (False).
    """
    INCOME_CLASS_1 = '1'
    INCOME_CLASS_2 = '2'
    INCOME_CLASS_3 = '3'
    INCOME_CLASS_4 = '4'
    INCOME_CLASS_5 = '5'
    INCOME_CLASS_6 = '6'
    INCOME_CLASS_SPECIAL = 'S'
    INCOME_CLASS_CHOICES = (
        (INCOME_CLASS_1, '1ST'),
        (INCOME_CLASS_2, '2ND'),
        (INCOME_CLASS_3, '3RD'),
        (INCOME_CLASS_4, '4TH'),
        (INCOME_CLASS_5, '5TH'),
        (INCOME_CLASS_6, '6TH'),
        (INCOME_CLASS_SPECIAL, 'SPECIAL'),
    )

    region = models.ForeignKey(
        Region,
        related_name='provinces',
        related_query_name='province',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Region'
    )
    income_class = models.CharField(max_length=1, choices=INCOME_CLASS_CHOICES,
                                    blank=True, null=False, verbose_name='Income Class')

    class Meta:
        db_table = 'ph_geography_province'
        verbose_name = 'Province'
        verbose_name_plural = 'Provinces'

    @property
    def island_group(self):
        return self.region.island_group


class Municipality(PhilippineGeography):
    """
    Model for municipalities and cities.

    Available fields are:
        * code - Unique geographical code for municipality.
        * name - Geographical name for municipality.
        * population - Population count based on 2015 POPCEN.
                        Null value means no data is available.
        * province - Province where the municipality is located.
        * is_city - Toggle to define whether the municipality is a city (True) or not (False).
        * is_capital - Toggle to define whether the city is a capital (True) or not (False).
        * city_class - City legal classification. Possible values are 'C' (component city),
                        'I' (independent component city), and 'H' (highly urbanized city).
                        Blank value means no data is available.
        * income_class - Income classification. Possible values are '1' (1st), '2' (2nd), '3' (3rd),
                          '4' (4th), '5' (5th), '6' (6th), and 'S' (Special).
                          Blank value means no data is available.
        * is_active - Toggle if municipality is active (True) or not (False).
    """
    CITY_CLASS_COMPONENT_CITY = 'C'
    CITY_CLASS_INDEPENDENT_COMPONENT_CITY = 'I'
    CITY_CLASS_HIGHLY_URBANIZED_CITY = 'H'
    CITY_CLASS_CHOICES = (
        (CITY_CLASS_COMPONENT_CITY, 'CC'),
        (CITY_CLASS_INDEPENDENT_COMPONENT_CITY, 'ICC'),
        (CITY_CLASS_HIGHLY_URBANIZED_CITY, 'HUC'),
    )
    INCOME_CLASS_1 = '1'
    INCOME_CLASS_2 = '2'
    INCOME_CLASS_3 = '3'
    INCOME_CLASS_4 = '4'
    INCOME_CLASS_5 = '5'
    INCOME_CLASS_6 = '6'
    INCOME_CLASS_SPECIAL = 'S'
    INCOME_CLASS_CHOICES = (
        (INCOME_CLASS_1, '1ST'),
        (INCOME_CLASS_2, '2ND'),
        (INCOME_CLASS_3, '3RD'),
        (INCOME_CLASS_4, '4TH'),
        (INCOME_CLASS_5, '5TH'),
        (INCOME_CLASS_6, '6TH'),
        (INCOME_CLASS_SPECIAL, 'SPECIAL'),
    )

    province = models.ForeignKey(
        Province,
        related_name='municipalities',
        related_query_name='municipality',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Province'
    )
    is_city = models.BooleanField(null=False, verbose_name='Is City')
    is_capital = models.BooleanField(null=False, verbose_name='Is Capital')
    city_class = models.CharField(max_length=1, choices=CITY_CLASS_CHOICES,
                                  blank=True, null=False, verbose_name='City Class')
    income_class = models.CharField(max_length=1, choices=INCOME_CLASS_CHOICES,
                                    blank=True, null=False, verbose_name='Income Class')

    class Meta:
        db_table = 'ph_geography_municipality'
        verbose_name = 'Municipality'
        verbose_name_plural = 'Municipalities'

    @property
    def region(self):
        return self.province.region

    @property
    def island_group(self):
        return self.province.region.island_group


class Barangay(PhilippineGeography):
    """
    Model for barangays.

    Available fields are:
        * code - Unique geographical code for barangay.
        * name - Geographical name for barangay.
        * population - Population count based on 2015 POPCEN.
                        Null value means no data is available.
        * municipality - Municipality where the barangay is located.
        * is_urban - Toggle to define whether the barangay is urban (True) or rural (False).
                      Null value means no data is available.
        * is_active - Toggle if barangay is active (True) or not (False).
    """
    municipality = models.ForeignKey(
        Municipality,
        related_name='barangays',
        related_query_name='barangays',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Barangay'
    )
    is_urban = models.NullBooleanField(null=True, verbose_name='Is Urban')

    class Meta:
        db_table = 'ph_geography_barangay'
        verbose_name = 'Barangay'
        verbose_name_plural = 'Barangays'

    @property
    def province(self):
        return self.municipality.province

    @property
    def region(self):
        return self.province.region

    @property
    def island_group(self):
        return self.region.island_group
