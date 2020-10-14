#!/usr/bin/env bash
rm -rf build/
rm -rf dist/
rm -rf django_ph_geography.egg-info/
python setup.py sdist bdist_wheel
