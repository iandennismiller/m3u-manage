#!/usr/bin/env python

import click

from m3u_manage.playlist import append_video, insert_video, delete_video, get_video, get_length

@click.group()
def queue():
    """
    Queue operations upon items within an m3u playlist.
    """
    pass

@queue.command('append', short_help='Update m3u by appending video to end.')
@click.argument('input_m3u', required=True)
@click.argument('video', required=True)
def do_append(input_m3u, video):
    """
    Update m3u by appending video to end.
    """
    append_video(input_m3u, video)

@queue.command('insert', short_help='Update m3u by inserting video at specified index.')
@click.argument('input_m3u', required=True)
@click.argument('video', required=True)
@click.argument('index', required=True)
def do_insert(input_m3u, video, index):
    """
    Update m3u by inserting video at specified index (0 for start).
    """
    insert_video(input_m3u, video, index)

@queue.command('delete', short_help='Update m3u by deleting video at specified index.')
@click.argument('input_m3u', required=True)
@click.argument('index', required=True)
def do_delete(input_m3u, index):
    """
    Update m3u by deleting video at specified index.
    """
    delete_video(input_m3u, index)

@queue.command('get', short_help='Print video at specified index.')
@click.argument('input_m3u', required=True)
@click.argument('index', required=True)
def do_get(input_m3u, index):
    """
    Print video at specified index.
    """
    get_video(input_m3u, index)

@queue.command('length', short_help='Get number of files in queue.')
@click.argument('input_m3u', required=True)
def do_length(input_m3u):
    """
    length IN.M3U: get number of files in queue
    """
    get_length(input_m3u)

queue.add_command(do_length)
queue.add_command(do_append)
queue.add_command(do_insert)
queue.add_command(do_delete)
queue.add_command(do_get)
