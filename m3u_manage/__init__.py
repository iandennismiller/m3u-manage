# -*- coding: utf-8 -*-
# m3u-manage (c) Ian Dennis Miller

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

def analyze(search_path, config_file):
    """
    analyze PATH tags.json: update syntax to just take a path, ignoring tags
    """
    # load config file, if provided
    if config_file:
        cfg = load_cfg(config_file)
        if 'tags' not in cfg:
            cfg['tags'] = []
    else:
        cfg = {
            'tags': []
        }

    word_list = []
    search_glob = "{}/**".format(search_path)
    for filename in glob.iglob(search_glob, recursive=True):
        if os.path.isfile(filename):
            stem = pathlib.Path(filename).stem.lower()
            word_list += [token for token in re.split(r'\W', stem) if len(token) > 1]

    # remove stopwords and tags
    filtered_words = [word for word in word_list if word not in stopwords.words('english')]
    filtered_words = [word for word in filtered_words if word not in cfg['tags']]

    raw = " ".join(filtered_words)
    bag = nltk.word_tokenize(raw)
    freqdist = FreqDist(bag)

    words_sorted = sorted(freqdist.items(), key =
        lambda kv:(kv[1], kv[0]))
    top_words = words_sorted[-30:]
    top_words.reverse()
    for word in top_words:
        print("{1}: {0}".format(*word))

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

def regularize(path):
    """
    regularize PATH: for all files in PATH, tolower filenames, fix garbage in filenames
    """
    [os.rename(f, f.lower()) for f in os.listdir(path)]

def decide(path, dest1, dest2):
    """
    decide PATH DEST1 DEST2: for all files in PATH, preview each and sort into DEST1 or DEST2 with a single keypress, then automatically advance
    """
    import pygame
    from moviepy.editor import VideoFileClip

    print("Press ESC to exit video. Use 'q' to quit deciding.")

    for filename in glob.glob(os.path.join(path, '*')):
        just_name = os.path.basename(filename)
        print(just_name)

        clip = VideoFileClip(filename)
        # use ESC key to exit
        clip.preview()
        pygame.display.quit()
        # pygame.quit()
        clip.close()

        print("Decide [z, x, or q]: ", end='')
        sys.stdout.flush()
        char = ''
        while char not in ['z', 'x', 'q']:
            char = getch.getche()
            print()

            if char == 'z':
                destination = os.path.join(dest1, just_name)
                print("move to {}".format(dest1))
                shutil.move(filename, destination)
            elif char == 'x':
                destination = os.path.join(dest2, just_name)
                print("move to {}".format(dest2))
                shutil.move(filename, destination)
            elif char == 'q':
                print("Exiting")
                sys.exit()

def gather(path, dest):
    """
    gather FROM_PATH TO_PATH: recursively move from_path into to_path, flattening directory hierarchy
    """
    search_glob = "{}/**".format(path)
    for filename in glob.iglob(search_glob, recursive=True):
        if os.path.isfile(filename):
            just_name = os.path.basename(filename)
            destination = os.path.join(dest, just_name)
            print(just_name)
            shutil.move(filename, destination)

def print_tags(cfg):
    print()
    idx = 1
    for tag in cfg['tags']:
        print("({}) {}".format(idx, tag), end=' ')
        idx += 1
        if idx > 9:
            print()
            break

def print_tag_prompt(cfg):
    print_tags(cfg)
    prompt = "Tag [1 - 9, n, q]: "
    print(prompt, end='')
    sys.stdout.flush()

def tag(path, config_file):
    import pygame
    from moviepy.editor import VideoFileClip

    # load config file, if provided
    if config_file:
        cfg = load_cfg(config_file)
        if 'tags' not in cfg:
            cfg['tags'] = []
    else:
        cfg = {
            'tags': []
        }

    search_glob = "{}/**".format(path)
    for filename in glob.iglob(search_glob, recursive=True):
        if os.path.isfile(filename):
            just_name = os.path.basename(filename)
            initial_name = just_name
            new_name = initial_name
            print(just_name)

            new_tags = []

            print_tags(cfg)

            clip = VideoFileClip(filename)
            # use ESC key to exit
            clip.preview()
            pygame.display.quit()
            # pygame.quit()
            clip.close()

            print_tag_prompt(cfg)

            char = ''
            while char not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'n', 'q']:
                char = getch.getche()
                print()

                if char == 'q':
                    print("\nExiting")
                    sys.exit()
                elif char == 'n':
                    if new_name != initial_name:
                        pathname = os.path.dirname(filename)
                        destination = os.path.join(pathname, new_name)
                        print("rename as '{}'".format(new_name))
                        shutil.move(filename, destination)
                    print("Next")
                elif char in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    tag_idx = int(char)-int('1')
                    tag = cfg['tags'][tag_idx]
                    new_name = tag + ' ' + new_name
                    new_tags.append(tag)

                    print("\nNew tags: {}".format(" ".join(new_tags)))
                    print_tag_prompt(cfg)
                    # prevent from breaking out of loop
                    char = ''
                else:
                    print("\nError: unrecognized input")
                    print_tag_prompt(cfg)
