#!/usr/bin/env python

import click

from m3u_manage.playlist import mesh, curate, repeat, append_video, insert_video, delete_video, get_video, get_summary, side_by_side, repack, combine, get_length, shuffle

@click.group()
def playlist():
    """
    Operations upon m3u playlists.
    """
    pass

@playlist.command('mesh', short_help='Combine playlists by interleaving items.')
@click.option('--outfile', '-o', required=True, help='New playlist file to create.')
@click.argument('filenames', nargs=-1, required=True)
def do_mesh(filenames, outfile):
    """
    Combine playlists by interleaving items.
    """
    mesh(filenames, outfile)

@playlist.command('repeat', short_help='Create playlist consisting of video repeated.')
@click.argument('output_m3u', required=True)
@click.argument('video', required=True)
@click.argument('times', required=True)
def do_repeat(output_m3u, video, times):
    """
    Create playlist consisting of video repeated.
    """
    repeat(output_m3u, video, times)

@playlist.command('summary', short_help='Print summary of m3u, with titles and durations.')
@click.argument('input_m3u', required=True)
def do_summary(input_m3u):
    """
    Print summary of m3u, with titles and durations.
    """
    get_summary(input_m3u)

@playlist.command('side-by-side', short_help='Convert all videos to sbs projection.')
@click.argument('input_m3u', required=True)
@click.argument('output_m3u', required=True)
def do_side_by_side(input_m3u, output_m3u):
    """
    Convert all videos to sbs projection.
    """
    side_by_side(input_m3u, output_m3u)

@playlist.command('repack', short_help='Convert all files in .m3u to specified format.')
@click.argument('input_m3u', required=True)
@click.argument('file_format', default='mp4', required=True)
def do_repack(input_m3u, file_format):
    """
    Convert all files in .m3u to specified format.
    """
    repack(input_m3u, file_format)

@playlist.command('combine', short_help='Concatenate all files into specified file.')
@click.argument('input_m3u', required=True)
@click.argument('output_file', required=True)
def do_combine(input_m3u, output_file):
    """
    combine --fade IN.M3U OUTPUT_FILE: using ffmpeg, concatenate all files into specified file.
    """
    combine(input_m3u, output_file)

@playlist.command('shuffle', short_help='Shuffle input.m3u into the specified output file.')
@click.argument('input_m3u', required=True)
@click.argument('output_file', required=True)
def do_shuffle(input_m3u, output_file):
    """
    shuffle IN.M3U OUT.M3U: shuffle input.m3u into the specified output file.
    """
    shuffle(input_m3u, output_file)

playlist.add_command(do_mesh)
playlist.add_command(do_repeat)
playlist.add_command(do_summary)
playlist.add_command(do_side_by_side)
playlist.add_command(do_repack)
playlist.add_command(do_combine)
playlist.add_command(do_shuffle)
