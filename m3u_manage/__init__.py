# -*- coding: utf-8 -*-
# m3u-manage (c) Ian Dennis Miller

import os
import re
import glob
import json
import m3u8
import nltk
import pathlib
import itertools
import operator
from nltk import ngrams, FreqDist
from nltk.corpus import stopwords

# https://stackoverflow.com/a/19295117
def distribute(sequence):
    """
    Enumerate the sequence evenly over the interval (0, 1).

    >>> list(distribute('abc'))
    [(0.25, 'a'), (0.5, 'b'), (0.75, 'c')]
    """
    m = len(sequence) + 1
    for i, x in enumerate(sequence, 1):
        yield i/m, x

# https://stackoverflow.com/a/19295117
def intersperse(*sequences):
    """
    Evenly intersperse the sequences.

    Based on https://stackoverflow.com/a/19293603/4518341

    >>> list(intersperse(range(10), 'abc'))
    [0, 1, 'a', 2, 3, 4, 'b', 5, 6, 7, 'c', 8, 9]
    >>> list(intersperse('XY', range(10), 'abc'))
    [0, 1, 'a', 2, 'X', 3, 4, 'b', 5, 6, 'Y', 7, 'c', 8, 9]
    >>> ''.join(intersperse('hlwl', 'eood', 'l r!'))
    'hello world!'
    """
    distributions = map(distribute, sequences)
    get0 = operator.itemgetter(0)
    for _, x in sorted(itertools.chain(*distributions), key=get0):
        yield x

def mesh(filenames, outfile):
    playlist = []

    for filename in filenames:
        print(filename)
        m3u8_obj = m3u8.load(filename)
        print(len(m3u8_obj.segments))

        new_items = [str(x) for x in m3u8_obj.segments]
        if not playlist:
            playlist = new_items
        else:
            playlist = list(intersperse(new_items, playlist))

    buf = ""
    for segment in playlist:
        buf += "{}\n".format(segment)

    with open(outfile, 'w') as f:
        f.write("#EXTM3U\n")
        f.write(buf)

    # return(buf)

def load_cfg(config):
    try:
        with open(config, 'r') as f:
            cfg = json.load(f)
    except FileNotFoundError:
        print("Error: config {} not found".format(config))
        return(-1)
    except json.decoder.JSONDecodeError as e:
        print("Error: cannot parse {}".format(config))
        print(e)
        return(-1)
    return(cfg)

def analyze(search_path):
    word_list = []
    search_glob = "{}/**".format(search_path)
    for filename in glob.iglob(search_glob, recursive=True):
        stem = pathlib.Path(filename).stem.lower()
        word_list += re.split(r'\W', stem)

    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    filtered_words = [word for word in filtered_words if word not in ['vids', '_db', 'mp4', '_', '1', '2']]

    raw = " ".join(filtered_words)
    bag = nltk.word_tokenize(raw)
    freqdist = FreqDist(bag)

    # words = [ x for (x, c) in freqdist.items() if c > 5 ]

    words_sorted = sorted(freqdist.items(), key =
        lambda kv:(kv[1], kv[0]))
    top_words = words_sorted[-30:]
    top_words.reverse()
    for word in top_words:
        print("{1}: {0}".format(*word))

def generate(config):
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
                    found = os.path.join(base_cwd, filename)
                    found = os.path.relpath(found, cfg["path"])
                    buf += "#EXTINF:0,{}\n".format(found)
                    buf += "{}\n".format(found)
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
            found = os.path.join(base_cwd, filename)
            found = os.path.relpath(found, cfg["path"])
            if found not in cfg['subdirs']:
                buf += "#EXTINF:0,{}\n".format(found)
                buf += "{}\n".format(found)

    filename = "{}/{}.m3u".format(cfg["path"], "unmatched")
    print("write {}".format(filename))
    with open(filename, "w") as f:
        f.write("#EXTM3U\n")
        f.write(buf)
