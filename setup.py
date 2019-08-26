from setuptools import setup,find_packages
from distutils.core import setup

setup(
    name='ScrapyDoo',
    version='0.1',
    description='Python code for building an academic journal & article database',
    url='http://github.com/phn409/ScrapyDoo',
    author='Peter H. Nguyen, David N. Purschke',
    author_email='ph1@ualberta.ca, purschke@ualberta.ca',
    packages=['ScrapyDoo','ScrapyDoo/scrapers','ScrapyDoo/db'],
    keywords='academic database graph citation network',
)
