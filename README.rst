Philippine Geography models for Django
======================================

**django-ph-geography** provide models for integrating Regions, Provinces, Municipalities, and Barangays in the Philippines.

Data retrieved from the Philippine Standard Geographic Code (PSGC) published by Philippine Statistics Authority (PSA) on March 31, 2020 (https://psa.gov.ph/classification/psgc/downloads/PSGC%20Publication%20March2020.xlsx).


Installation
------------

Installing using `pip <https://pip.pypa.io/en/stable/quickstart/>`_:

.. code-block:: console

    pip install django-ph-geography


Add ``ph_geography`` to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'ph_geography',
    ]


Migrate app models to database:

.. code-block:: console

    python manage.py migrate ph_geography


Load initial data:

.. code-block:: console

    python manage.py loaddata regions.json --app ph_geography
    python manage.py loaddata provinces.json --app ph_geography
    python manage.py loaddata municipalities.json --app ph_geography
    python manage.py loaddata barangays.json --app ph_geography



Models
------

ph_geography.models.Region
^^^^^^^^^^^^^^^^^^^^^^^^^^

Model for regions. Available fields are:

- ``code`` (``CharField<max_length=10, unique=True, null=False>``): Unique geographical code for region.
- ``name`` (``CharField<max_length=100, null=False)>``): Geographical name for region.
- ``population`` (``PositiveIntegerField<null=True>``): Population count based on 2015 POPCEN. Null value means no data is available.
- ``island_group`` (``CharField<max_length=1, choices=ISLAND_GROUP_CHOICES, null=False>``): Island group where the region is located. Possible values are based on items in model property ``ISLAND_GROUP_CHOICES``:
    + ``ISLAND_GROUP_LUZON`` (``'L'``) - Luzon
    + ``ISLAND_GROUP_VISAYAS`` (``'V'``) - Visayas
    + ``ISLAND_GROUP_MINDANAO`` (``'M'``) - Mindanao


ph_geography.models.Province
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Model for provinces. Available fields are:

- ``code`` (``CharField<max_length=10, unique=True, null=False>``): Unique geographical code for region.
- ``name`` (``CharField<max_length=100, null=False)>``): Geographical name for region.
- ``population`` (``PositiveIntegerField<null=True>``): Population count based on 2015 POPCEN. Null value means no data is available.
- ``region`` (``ForeignKey<Region, related_name='provinces', related_query_name='province', null=False, on_delete=models.CASCADE>``): Region where province is located.
- ``income_class`` (``CharField<max_length=1, choices=INCOME_CLASS_CHOICES, null=False, blank=True>``): Income classification. Blank value means no data is available. Possible values are based on items in model property ``INCOME_CLASS_CHOICES``:
    + ``INCOME_CLASS_1`` (``'1'``) - 1st
    + ``INCOME_CLASS_2`` (``'2'``) - 2nd
    + ``INCOME_CLASS_3`` (``'3'``) - 3rd
    + ``INCOME_CLASS_4`` (``'4'``) - 4th
    + ``INCOME_CLASS_5`` (``'5'``) - 5th
    + ``INCOME_CLASS_6`` (``'6'``) - 6th
    + ``INCOME_CLASS_SPECIAL`` (``'S'``) - Special


ph_geography.models.Municipality
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Model for municipalities and cities. Available fields are:

- ``code`` (``CharField<max_length=10, unique=True, null=False>``): Unique geographical code for region.
- ``name`` (``CharField<max_length=100, null=False)>``): Geographical name for region.
- ``population`` (``PositiveIntegerField<null=True>``): Population count based on 2015 POPCEN. Null value means no data is available.
- ``province`` (``ForeignKey<Province, related_name='municipalities', related_query_name='municipality', null=False, on_delete=models.CASCADE>``): Province where municipality is located.
- ``income_class`` (``CharField<max_length=1, choices=INCOME_CLASS_CHOICES, null=False, blank=True>``): Income classification. Blank value means no data is available. Possible values are based on items in model property ``INCOME_CLASS_CHOICES``:
    + ``INCOME_CLASS_1`` (``'1'``) - 1st
    + ``INCOME_CLASS_2`` (``'2'``) - 2nd
    + ``INCOME_CLASS_3`` (``'3'``) - 3rd
    + ``INCOME_CLASS_4`` (``'4'``) - 4th
    + ``INCOME_CLASS_5`` (``'5'``) - 5th
    + ``INCOME_CLASS_6`` (``'6'``) - 6th
    + ``INCOME_CLASS_SPECIAL`` (``'S'``) - Special
- ``is_city`` (``BooleanField<null=False>``): Toggle to define whether the municipality is a city (``True``) or not (``False``)
- ``is_capital``: (``BooleanField<null=False>``): Toggle to define whether the municipality is a capital (``True``) or not (``False``)
- ``city_class`` (``CharField<max_length=1, choices=CITY_CLASS_CHOICES, null=False, blank=True>``): City legal classification. Blank value means no data is available. Possible values are based on items in model property ``CITY_CLASS_CHOICES``:
    + ``CITY_CLASS_COMPONENT_CITY`` (``'C'``) - CC
    + ``CITY_CLASS_INDEPENDENT_COMPONENT_CITY`` (``'I'``) - ICC
    + ``CITY_CLASS_HIGHLY_URBANIZED_CITY`` (``'H'``) - HUC


ph_geography.models.Barangay
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Model for barangays. Available fields are:

- ``code`` (``CharField<max_length=10, unique=True, null=False>``): Unique geographical code for region.
- ``name`` (``CharField<max_length=100, null=False)>``): Geographical name for region.
- ``population`` (``PositiveIntegerField<null=True>``): Population count based on 2015 POPCEN. Null value means no data is available.
- ``municipality`` (``ForeignKey<Municipality>, related_name='barangays', related_query_name='barangay', null=False, on_delete=models.CASCADE>``): Municipality where barangay is located.
- ``is_urban`` (``BooleanField<null=False>``): Toggle to define whether the barangay is urban (``True``) or rural (``False``). Null value means no data is available.
