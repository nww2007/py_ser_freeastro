#!/usr/bin/env python3
# Created: 15.06.2019
# Copyright (c) 2019 Vladimir Nekrasov
# License: The MIT License


from setuptools import setup, find_packages
from os.path import join, dirname
from setuptools.dist import Distribution


def get_version():
    v = {}
    # do not import ezdxf, because required packages may not be installed yet
    for line in open('./py_ser_freeastro/version.py').readlines():
        if line.strip().startswith('__version__'):
            exec(line, v)
            return v['__version__']
    raise IOError('__version__ string not found')


class BinaryDistribution(Distribution):
    def is_pure(self):
        return False


setup(name='py_set_freeastro',
      version=get_version(),
      description='A Python package to create/manipulate SER astro images.',
      author='Vladimir Nekrasov',
      author_email='nww2007@mail.ru',
      keywords=['SER', 'astroimage'],
      platforms='OS Independent',
      license="MIT",
      packages=find_packages(),
      long_description=open(join(dirname(__file__), 'README.md')).read(),
      include_package_data=True,
      distclass=BinaryDistribution,
      install_requires=['progress']
)
