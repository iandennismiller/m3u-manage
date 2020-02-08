m3u-manage
=============

https://m3u-manage.readthedocs.io

Tools to create amd manage an m3u playlist

.. image:: https://img.shields.io/github/stars/iandennismiller/m3u-manage.svg?style=social&label=GitHub
    :target: https://github.com/iandennismiller/m3u-manage

.. image:: https://img.shields.io/pypi/v/m3u-manage.svg
    :target: https://pypi.python.org/pypi/m3u-manage

.. image:: https://readthedocs.org/projects/m3u-manage/badge/?version=latest
    :target: http://m3u-manage.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://travis-ci.org/iandennismiller/m3u-manage.svg?branch=master
    :target: https://travis-ci.org/iandennismiller/m3u-manage

Overview
--------

Installation
^^^^^^^^^^^^

Python pip
~~~~~~~~~~

::

    pip install m3u-manage

Usage
^^^^^

Analyze a playlist for the most common filename terms.

::

    m3um analyze --config example.json

Generate a playlist based on files in a folder.

::

    m3um generate --config example.json

Interleaves playlists by inserting with even-spacing.

::

    m3um mesh --config example.json

example.json
^^^^^^^^^^^^
::

    {
        "path": ".",
        "subdirs": ["videos"],
        "patterns": {
            "cars": "(car|auto|sedan)",
            "trucks": "(truck|bus|shuttle)",
            "planes": {
                "include": "(jet|plane|rocket)",
                "exclude": "shuttle"
            }
        }
    }


Documentation
^^^^^^^^^^^^^

https://m3u-manage.readthedocs.io
