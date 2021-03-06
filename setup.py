import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-related-models',
    version='0.2',
    license="BSD",
    packages=find_packages(),
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
