import os
import re
import sys
import glob
import json
import m3u8
import nltk
import getch
import shutil
import pathlib
from nltk import ngrams, FreqDist
from nltk.corpus import stopwords

from . import load_cfg
from .util import intersperse

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
            rel_path = os.path.relpath(found, cfg["path"])
            if rel_path not in cfg['subdirs'] and os.path.isfile(full_path):
                buf += "#EXTINF:0,{}\n".format(rel_path)
                buf += "{}\n".format(rel_path)

    filename = "{}/{}.m3u".format(cfg["path"], "unmatched")
    print("write {}".format(filename))
    with open(filename, "w") as f:
        f.write("#EXTM3U\n")
        f.write(buf)

def repeat(output_m3u, video, times):
    pass
