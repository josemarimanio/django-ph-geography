Philippine Geography models for Django
======================================

**django-ph-geography** provide models for integrating Regions, Provinces, Municipalities, and Barangays in the Philippines.


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
