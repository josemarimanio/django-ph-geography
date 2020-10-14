import io

from setuptools import find_packages
from setuptools import setup

from ph_geography import __version__

with io.open('README.rst', 'rt', encoding='utf8') as f:
    README = f.read()

install_requires = ['django>=1.11', ]
tests_require = ['django-migration-testcase==0.0.15', ]
extras_require = {'test': tests_require, }

setup(
    name='django-ph-geography',
    version=__version__,
    description='Philippine Geography models for Django',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/josemarimanio/django-ph-geography/',
    project_urls={
        'Source Code': 'https://github.com/josemarimanio/django-ph-geography/',
    },
    author='Jose Mari Manio',
    author_email='josemari.manio@tutamail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.4',
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
)
