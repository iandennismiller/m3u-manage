#!/usr/bin/env python

import sys
sys.path.insert(0, '.')

import click
from m3u_manage.filesystem import regularize, analyze, decide, gather, tag
from m3u_manage.download import download_video

@click.group()
def _dir():
    """
    Operations upon a filesystem path.
    """
    pass

@_dir.command('download', short_help='Download a video or playlist with youtube-dl.')
@click.argument('url', required=True)
@click.argument('output_path', required=True)
def do_download(url, output_path):
    """
    download URL OUTPUT_PATH: Download video(s) with youtube-dl and normalize volume.
    """
    download_video(url, output_path)

@_dir.command('analyze', short_help='Analyze directory for keywords.')
@click.option('--config', '-c', help='Config file containing tags.')
@click.argument('directory', required=True)
def do_analyze(directory, config):
    """
    Analyze directory for keywords.
    """
    analyze(directory, config)

@_dir.command('curate', short_help='Automatically curate videos into playlists.')
@click.option('--config', required=True, help='Curation configuration filename.')
def do_curate(config):
    """
    Automatically curate videos into playlists.
    """
    curate(config)

@_dir.command('decide', short_help='Perform sorting decisions about videos.')
@click.argument('input_path', required=True)
@click.argument('dest1', required=True)
@click.argument('dest2', required=True)
def do_decide(input_path, dest1, dest2):
    """
    Perform sorting decisions about videos.
    """
    decide(input_path, dest1, dest2)

@_dir.command('regularize', short_help='Regularize filenames in a directory.')
@click.argument('directory', required=True)
def do_regularize(directory):
    """
    Regularize filenames in a directory.
    """
    regularize(directory)

@_dir.command('gather', short_help='Recursively move from DIRECTORY into DESTINATION.')
@click.argument('directory', required=True)
@click.argument('destination', required=True)
def do_gather(directory, destination):
    """
    Recursively move from DIRECTORY into DESTINATION, flattening directory hierarchy.
    """
    gather(directory, destination)

@_dir.command('tag', short_help='Tag path in directory.')
@click.option('--config', '-c', help='Config file containing tags.')
@click.argument('directory', required=True)
def do_tag(directory, config):
    """
    TAG: use hotkeys to add tags to path
    """
    tag(directory, config)

_dir.add_command(do_analyze)
_dir.add_command(do_curate)
_dir.add_command(do_decide)
_dir.add_command(do_regularize)
_dir.add_command(do_gather)
_dir.add_command(do_tag)
_dir.add_command(do_download)
