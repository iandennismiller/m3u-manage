import ffmpeg

def side_by_side_video(infile, outfile):
    in1 = ffmpeg.input(infile)

    v1 = in1.video.filter('scale', width=-1, height=720)\
        .filter('crop', 640, 720)\
        .filter('stereo3d', 'al', 'sbsl')

    a1 = in1.audio

    out = ffmpeg.output(v1, a1, outfile).overwrite_output()
    out.run()
