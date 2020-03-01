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

def regularize(path):
    """
    regularize PATH: for all files in PATH, tolower filenames, fix garbage in filenames
    """
    [os.rename(f, f.lower()) for f in os.listdir(path)]

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
