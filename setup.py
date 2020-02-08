# -*- coding: utf-8 -*-
# m3u-manage (c) Ian Dennis Miller

import re
import os
import codecs
from setuptools import setup
from setuptools import find_packages


def read(*rnames):
    return codecs.open(os.path.join(os.path.dirname(__file__), *rnames), 'r', 'utf-8').read()


def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, read('m3u_manage/__meta__.py'))
    return strval


setup(
    version=grep('__version__'),
    name='m3u-manage',
    description="Tools to create amd manage an m3u playlist",
    packages=find_packages(),
    scripts=[
        'bin/m3um',
    ],
    long_description=read('Readme.rst'),
    classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    include_package_data=True,
    keywords='',
    author=grep('__author__'),
    author_email=grep('__email__'),
    url=grep('__url__'),
    install_requires=read('requirements.txt'),
    license='MIT',
    zip_safe=False,
)
