import os
import re
import sys
import glob
import json
import m3u8
import nltk
import getch
import ffmpeg
import shutil
import random
import pathlib
from nltk import ngrams, FreqDist
from nltk.corpus import stopwords

from . import load_cfg
from .util import intersperse
from .video import side_by_side_video, repack_video, concatenate_video

stub_m3u_tmpl = """
#EXTM3U
#EXTINF:0,{video}
{video}
"""

def combine_m3us(m3u_filenames):
    playlist = []

    for filename in m3u_filenames:
        print(filename)
        m3u8_obj = m3u8.load(filename)
        print("found: {}".format(len(m3u8_obj.segments)))

        new_items = [str(x) for x in m3u8_obj.segments]
        if not playlist:
            playlist = new_items
        else:
            playlist = list(intersperse(new_items, playlist))

    return(playlist)

def write_m3u(outfile, buf):
    with open(outfile, 'w') as f:
        f.write("#EXTM3U\n")
        f.write(buf)

def mesh(filenames, outfile):
    playlist = combine_m3us(filenames)

    buf = ""
    for segment in playlist:
        buf += "{}\n".format(segment)

    write_m3u(outfile, buf)
    print("wrote {}".format(outfile))

def curate(config):
    cfg = load_cfg(config)
    base_cwd = os.getcwd()

    listing = {}
    for search_path in cfg['subdirs']:
        search_glob = "{}/{}/**".format(cfg["path"], search_path)
        for filename in glob.iglob(search_glob, recursive=True):
            listing[filename] = False

    for name, pattern in cfg['patterns'].items():
        if type(pattern) is dict:
            pattern_include = pattern["include"]
            pattern_exclude = pattern["exclude"]
        else:
            pattern_include = pattern
            pattern_exclude = None

        buf = ""
        for search_path in cfg['subdirs']:
            search_glob = "{}/{}/**".format(cfg["path"], search_path)
            for filename in glob.iglob(search_glob, recursive=True):
                was_found = False

                if pattern_exclude:
                    if re.search(pattern_include, filename, re.IGNORECASE) and not re.search(pattern_exclude, filename, re.IGNORECASE):
                        was_found = True
                        listing[filename] = True
                else:
                    if re.search(pattern_include, filename, re.IGNORECASE):
                        was_found = True
                        listing[filename] = True

                if was_found:
                    full_path = os.path.join(base_cwd, filename)
                    rel_path = os.path.relpath(full_path, cfg["path"])
                    if os.path.isfile(full_path):
                        buf += "#EXTINF:0,{}\n".format(rel_path)
                        buf += "{}\n".format(rel_path)
        if buf != "":
            filename = "{}/{}.m3u".format(cfg["path"], name)
            print("write {}".format(filename))
            with open(filename, "w") as f:
                f.write("#EXTM3U\n")
                f.write(buf)

    # write unmatched
    buf = ""
    for filename in listing:
        if listing[filename] is False:
            full_path = os.path.join(base_cwd, filename)
            rel_path = os.path.relpath(full_path, cfg["path"])
            if rel_path not in cfg['subdirs'] and os.path.isfile(full_path):
                buf += "#EXTINF:0,{}\n".format(rel_path)
                buf += "{}\n".format(rel_path)

    filename = "{}/{}.m3u".format(cfg["path"], "unmatched")
    print("write {}".format(filename))
    with open(filename, "w") as f:
        f.write("#EXTM3U\n")
        f.write(buf)

def repeat(output_m3u, video, times):
    """
    repeat OUT.M3U VIDEO N-TIMES: create playlist consisting of video repeated
    """
    buf = ""

    for i in range(0, int(times)):
        buf += "#EXTINF:0,{}\n".format(video)
        buf += "{}\n".format(video)

    with open(output_m3u, "w") as f:
        f.write("#EXTM3U\n")
        f.write(buf)

def append_video(input_m3u, video):
    """
    append IN.M3U VIDEO: update m3u by appending video to end
    """
    try:
        m3u8_obj = m3u8.load(input_m3u)
        new_segment = m3u8.Segment(uri=video, title=video, duration=0)
        print("Append {} to end of playlist".format(video))
        m3u8_obj.segments.append(new_segment)
        with open(input_m3u, "w") as f:
            f.write(m3u8_obj.dumps())
    except:
        with open(input_m3u, "w") as f:
            f.write(stub_m3u_tmpl.format(video=video))

def insert_video(input_m3u, video, index):
    """
    insert IN.M3U INDEX VIDEO: update m3u by inserting video at specified index (0 for start)
    """
    m3u8_obj = m3u8.load(input_m3u)

    new_segment = m3u8.Segment(uri=video, title=video, duration=0)
    segment = m3u8_obj.segments[int(index)]

    print("Inserting {} before {}".format(video, segment.uri))
    m3u8_obj.segments.insert(int(index), new_segment)

    with open(input_m3u, "w") as f:
        f.write(m3u8_obj.dumps())

def delete_video(input_m3u, index):
    """
    delete IN.M3U INDEX: update m3u by deleting video at specified index
    """
    m3u8_obj = m3u8.load(input_m3u)
    segment = m3u8_obj.segments[int(index)]

    print("Deleting {}".format(segment.uri))
    del(m3u8_obj.segments[int(index)])

    with open(input_m3u, "w") as f:
        f.write(m3u8_obj.dumps())

def get_video(input_m3u, index):
    """
    get IN.M3U INDEX: print video at specified index
    """
    m3u8_obj = m3u8.load(input_m3u)
    segment = m3u8_obj.segments[int(index)]
    print(segment)

def get_summary(input_m3u):
    """
    summary IN.M3U: print summary of m3u, with titles and durations
    """
    m3u8_obj = m3u8.load(input_m3u)

    print("Summary of: {}".format(input_m3u))
    print("Number of files in m3u: {}\n".format(len(m3u8_obj.segments)))

    idx = 0
    for segment in m3u8_obj.segments:
        print("{}.\t{}s\t{}".format(idx, segment.duration, segment.uri))
        idx += 1
        
def side_by_side(input_m3u, output_m3u):
    """
    side-by-side IN.M3U OUT.M3U: using ffmpeg, convert all videos to sbs projection
    """
    m3u8_obj = m3u8.load(input_m3u)

    for segment in m3u8_obj.segments:
        filename = segment.uri
        if os.path.isfile(filename):
            pathname = os.path.dirname(filename)
            basename = os.path.basename(filename)

            new_filename = os.path.join(pathname, "sbs " + basename)
            side_by_side_video(filename, new_filename)

            segment.uri = new_filename
            segment.title = new_filename

    with open(output_m3u, "w") as f:
        f.write(m3u8_obj.dumps())

def repack(input_m3u, file_format="mp4"):
    """
    repack IN.M3U FORMAT: using ffmpeg, convert all files in .m3u to specified format
    """
    m3u8_obj = m3u8.load(input_m3u)

    any_changed = False

    for segment in m3u8_obj.segments:
        filename = segment.uri
        if os.path.isfile(filename):
            pathname = os.path.dirname(filename)
            no_ext = os.path.splitext(filename)[0]

            probe = ffmpeg.probe(filename)
            if file_format not in probe['format']['format_name'].split(','):
                any_changed = True
                new_filename = os.path.join(pathname, no_ext + "." + file_format)
                segment.uri = new_filename
                segment.title = new_filename
                print("converting {} to {}".format(filename, new_filename))
                repack_video(filename, new_filename, file_format)

    if any_changed:
        with open(input_m3u, "w") as f:
            f.write(m3u8_obj.dumps())
    else:
        print("Entire playlist is already {} format.".format(file_format))

def get_length(input_m3u):
    """
    length IN.M3U: get number of files in playlist
    """
    m3u8_obj = m3u8.load(input_m3u)
    print("{}".format(len(m3u8_obj.segments)))

def combine(input_m3u, output_file):
    """
    combine --fade IN.M3U OUT.MP4: using ffmpeg, concatenate all files into specified file
    """
    m3u8_obj = m3u8.load(input_m3u)

    filename_list = []
    for segment in m3u8_obj.segments:
        if os.path.isfile(segment.uri):
            filename_list.append(segment.uri)

    if len(filename_list) > 0:
        concatenate_video(filename_list, output_file)

def shuffle(input_m3u, output_m3u):
    """
    shuffle IN.M3U OUT.M3U: shuffle input.m3u into the specified output file.
    """
    m3u8_obj = m3u8.load(input_m3u)
    random.shuffle(m3u8_obj.segments)
    with open(output_m3u, "w") as f:
        f.write(m3u8_obj.dumps())
