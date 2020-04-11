from __future__ import unicode_literals
import youtube_dl
import os
import tempfile
import shutil
import glob
from pathlib import Path

# https://github.com/ytdl-org/youtube-dl#embedding-youtube-dl

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_video(url, output_path, playlist_start=1):
    tmp_path = tempfile.mkdtemp()
    print("Downloading to temporary path: {}".format(tmp_path))

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'nooverwrites': True,
        'sleep_interval': 15,
        'max_sleep_interval': 30,
        'playliststart': playlist_start,
        'merge_output_format': 'mp4',
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'outtmpl': tmp_path + f'/%(title)s.mp4',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Begin volume normalization")
    from ffmpeg_normalize._ffmpeg_normalize import FFmpegNormalize
    # -ext mp4 \
    ffnorm = FFmpegNormalize(
        output_format='mp4',
        audio_codec='aac',
    )

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for input_file in glob.glob(tmp_path + '/*.mp4'):
        filename = Path(input_file).name
        output_file = os.path.join(output_path, filename)
        print(output_file)
        ffnorm.add_media_file(input_file, output_file)

    ffnorm.run_normalization()

    shutil.rmtree(tmp_path)
    print("End normalization")
