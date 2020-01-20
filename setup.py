import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

setup(
    name='django-related-models',
    version='0.1',
    packages=['django_related_models'],
    description='A related model sidebar for Django Admin',
    long_description=README,
    author='Nick Nelson',
    author_email='whoisnicknelson@gmail.com',
    url='https://github.com/nicknelson/django-related-models/',
    license='MIT',
    install_requires=[
        'Django>=2.0',
    ]
)
