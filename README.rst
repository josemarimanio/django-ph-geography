.. image:: https://img.shields.io/pypi/v/django-ph-geography
    :alt: PyPi
    :target: https://pypi.org/project/django-ph-geography

.. image:: https://img.shields.io/pypi/pyversions/django-ph-geography
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/django-ph-geography

.. image:: https://img.shields.io/pypi/djversions/django-ph-geography
    :alt: PyPI - Django Version
    :target: https://pypi.org/project/django-ph-geography

.. image:: https://travis-ci.com/josemarimanio/django-ph-geography.svg?branch=main
    :alt: Travis CI
    :target: https://travis-ci.com/josemarimanio/django-ph-geography

.. image:: https://www.codefactor.io/repository/github/josemarimanio/django-ph-geography/badge
    :alt: CodeFactor Grade
    :target: https://www.codefactor.io/repository/github/josemarimanio/django-ph-geography

.. image:: https://img.shields.io/codecov/c/github/josemarimanio/django-ph-geography
    :alt: Codecov
    :target: https://codecov.io/gh/josemarimanio/django-ph-geography

.. image:: https://img.shields.io/github/license/josemarimanio/django-ph-geography
    :alt: License - MIT
    :target: https://github.com/josemarimanio/django-ph-geography/blob/master/LICENSE


Philippine Geography models for Django
======================================

**django-ph-geography** provides models for integrating regions, provinces, municipalities, and barangays in the Philippines.

Data retrieved from the Philippine Standard Geographic Code (PSGC) published by Philippine Statistics Authority (PSA) on March 31, 2020 (https://psa.gov.ph/classification/psgc/downloads/PSGC%20Publication%20March2020.xlsx).


Table of Contents
-----------------
- `Installation <#installation>`_
- `Models <#models>`_
- `Monkey Patching <#monkey-patching>`_


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

    python manage.py phgeofixtures


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
- ``is_active`` (``BooleanField<null=False, default=True>``): Toggle if region is active (``True``) or not (``False``).


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
- ``is_active`` (``BooleanField<null=False, default=True>``): Toggle if province is active (``True``) or not (``False``).


Available properties:

- ``island_group``: Reference to ``Region`` field ``island_group``.


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
- ``is_city`` (``BooleanField<null=False>``): Toggle to define whether the municipality is a city (``True``) or not (``False``).
- ``is_capital`` (``BooleanField<null=False>``): Toggle to define whether the municipality is a capital (``True``) or not (``False``).
- ``city_class`` (``CharField<max_length=1, choices=CITY_CLASS_CHOICES, null=False, blank=True>``): City legal classification. Blank value means no data is available. Possible values are based on items in model property ``CITY_CLASS_CHOICES``:

  + ``CITY_CLASS_COMPONENT_CITY`` (``'C'``) - CC
  + ``CITY_CLASS_INDEPENDENT_COMPONENT_CITY`` (``'I'``) - ICC
  + ``CITY_CLASS_HIGHLY_URBANIZED_CITY`` (``'H'``) - HUC
- ``is_active`` (``BooleanField<null=False, default=True>``): Toggle if municipality is active (``True``) or not (``False``).


Available properties:

- ``island_group``: Reference to ``Region`` field ``island_group``.
- ``region``: Reference to ``province`` field ``region``.


ph_geography.models.Barangay
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Model for barangays. Available fields are:

- ``code`` (``CharField<max_length=10, unique=True, null=False>``): Unique geographical code for region.
- ``name`` (``CharField<max_length=100, null=False)>``): Geographical name for region.
- ``population`` (``PositiveIntegerField<null=True>``): Population count based on 2015 POPCEN. Null value means no data is available.
- ``municipality`` (``ForeignKey<Municipality>, related_name='barangays', related_query_name='barangay', null=False, on_delete=models.CASCADE>``): Municipality where barangay is located.
- ``is_urban`` (``NullBooleanField<null=False>``): Toggle to define whether the barangay is urban (``True``) or rural (``False``). Null value means no data is available.
- ``is_active`` (``BooleanField<null=False, default=True>``): Toggle if barangay is active (``True``) or not (``False``).


Available properties:

- ``island_group``: Reference to ``Region`` field ``island_group``.
- ``province``: Reference to ``municipality`` field ``province``.
- ``region``: Reference to property ``province`` field ``region``.



Monkey Patching
---------------

After migrating the models and loading the initial data through fixtures, you can monkey patch (*if you're into it*) **django-ph-geography** models using the provided methods to suit your needs:


Adding new fields
^^^^^^^^^^^^^^^^^

You can use the custom method ``add_field`` provided by abstract model class ``ph_geography.models.PhilippineGeography`` to add fields to the models provided.
Using the said method to the abstract model will apply the action to all subclasses.

Example:

.. code-block:: python

    from django.db import models

    from ph_geography.models import PhilippineGeography
    from ph_geography.models import Region


    # Add field to Region, Province, Municipality, Barangay, and any subclass models of PhilippineGeography
    PhilippineGeography.add_field('all_models', models.BooleanField(null=True))

    # Add field 'single_model' to Region
    Region.add_field('single_model', models.BooleanField(null=True))


Removing existing fields
^^^^^^^^^^^^^^^^^^^^^^^^

You can use the custom method ``remove_field`` provided by abstract model class ``ph_geography.models.PhilippineGeography`` to remove fields to the models provided.
Using the same method to the abstract model will apply the action to all subclasses.

Example:

.. code-block:: python

    from ph_geography.models import PhilippineGeography
    from ph_geography.models import Municipality
    from ph_geography.models import Region


    # Remove field to Region, Province, Municipality, Barangay, and any subclass models of PhilippineGeography
    PhilippineGeography.remove_field('population')

    # Remove field 'island_group' from Region
    Region.remove_field('island_group')

    # Multiple fields to remove are supported
    Municipality.remove_field('is_city', 'is_capital')
