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

::

    m3um analyze ./TV
    m3um generate --config ./example.json
    m3um mesh -o mesh.m3u TV/*.m3u

Analyze a playlist for the most common terms appearing in filenames.

::

    m3um analyze DIRECTORY_NAME

Generate playlists based on the inclusion and exclusion criteria in the provided .json file.

::

    m3um generate --config example.json

Create interleaved playlists by inserting from playlists with even spacing.

::

    m3um mesh -o OUTPUT.m3u FILE1.m3u FILE2.m3u FILE3.m3u ...

example.json
^^^^^^^^^^^^

When using the generate command, a series of expressions is provided in a .json file to indicate which playlists to generate.

The following `example.json` creates three .m3u files based on the videos present in the /TV directory.
The cars and trucks playlists will contain any filename that matches the regular expressions.

The planes example specifies criteria for inclusion and exclusion, both as regular expressions.
According to the exclusion criteria, all shuttles belong in the trucks playlist.

::

    {
        "path": ".",
        "subdirs": ["TV"],
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
