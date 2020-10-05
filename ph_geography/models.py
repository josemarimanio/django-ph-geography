from django.db import models


class AbstractGeographyModel(models.Model):
    """
    Abstract model for common geographical fields.

    Available fields are:
        * code - Unique geographical code.
        * name - Geographical name.
        * population - Population count based on 2015 POPCEN.
                        Null value  means no data is available.
    """
    code = models.CharField(max_length=10, unique=True, null=False, verbose_name='Code')
    name = models.CharField(max_length=100, null=False, verbose_name='Name')
    population = models.PositiveIntegerField(null=True, verbose_name='Population')

    class Meta:
        abstract = True

    def __repr__(self):
        return '<Code: {code}, Name: {name}>'.format(
            code=self.code,
            name=self.name,
        )

    def __str__(self):
        return self.name


class Region(AbstractGeographyModel):
    """
    Model for regions.

    Available fields are:
        * code - Unique geographical code for region.
        * name - Geographical name for region.
        * population - Population count based on 2015 POPCEN.
                        Null value means no data is available.
        * island_group - Island group where the region is located. Possible values are 'L' (for Luzon),
                         'V' (for Visayas), and 'M' (for Mindanao).
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


class Province(AbstractGeographyModel):
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


class Municipality(AbstractGeographyModel):
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


class Barangay(AbstractGeographyModel):
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
    """
    municipality = models.ForeignKey(
        Municipality,
        related_name='barangays',
        related_query_name='barangays',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Barangay'
    )
    is_urban = models.BooleanField(null=True, verbose_name='Is Urban')

    class Meta:
        db_table = 'ph_geography_barangay'
        verbose_name = 'Barangay'
        verbose_name_plural = 'Barangays'
