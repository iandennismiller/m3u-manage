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

::

    pip install m3u-manage

Usage
^^^^^

Analyze
"""""""

Analyze a playlist for the most common terms appearing in filenames.

::

    m3um analyze DIRECTORY_NAME

Produces output like:

::

    m3u-manage 0.2.2
    90: cbc
    47: true
    47: season
    45: patrol

Mesh
""""

Create interleaved playlists by inserting from playlists with even spacing.

::

    m3um mesh -o OUTPUT.m3u FILE1.m3u FILE2.m3u FILE3.m3u ...

Produces output like:

::

    m3u-manage 0.2.2
    TV/cars.m3u
    9
    TV/trucks.m3u
    27
    TV/planes.m3u
    31
    wrote OUTPUT.m3u

Curate
""""""""

Curate playlists based on the inclusion and exclusion criteria in the provided .json file.

::

    m3um curate --config example.json

Produces output like:

::

    m3u-manage 0.2.2
    write TV/cars.m3u
    write TV/trucks.m3u
    write TV/planes.m3u

example.json
""""""""""""

When using the curate command, a series of expressions is provided in a .json file to indicate which playlists to generate.

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

Recipes
^^^^^^^

Downloading from youtube and normalizing volume
"""""""""""""""""""""""""""""""""""""""""""""""

::

    function media_download {
        URL=$1
        youtube-dl \
            -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' \
            --merge-output-format mp4 \
            --no-overwrites \
            --sleep-interval 15 \
            --max-sleep-interval 30 \
            --playlist-start 1 \
            "$URL"
        ~/.local/bin/ffmpeg-normalize *.mp4 \
            --progress \
            --output-format mp4 \
            -ext mp4 \
            -c:a aac && \
            mkdir .old && \
            mv *.mp4 .old && \
            mv normalized/*.mp4 . && \
            rmdir normalized
    }

Documentation
^^^^^^^^^^^^^

https://m3u-manage.readthedocs.io
