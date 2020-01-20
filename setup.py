import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-related-models',
    version='0.1',
    license="BSD",
    packages=['django_related_models'],
    description='A related model sidebar for Django Admin',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nick Nelson',
    author_email='nick.eugene.nelson@gmail.com',
    url='https://github.com/nicknelson/django-related-models/',
    install_requires=[
        'Django>=2.0',
    ]
)
