import ffmpeg

def side_by_side_video(infile, outfile):
    in1 = ffmpeg.input(infile)

    v1 = in1.video.filter('scale', width=-1, height=720)\
        .filter('crop', 640, 720)\
        .filter('stereo3d', 'al', 'sbsl')

    a1 = in1.audio

    out = ffmpeg.output(v1, a1, outfile).overwrite_output()
    out.run()

def repack_video(infile, outfile, file_format='mp4'):
    in1 = ffmpeg.input(infile)

    # v1 = in1.video
    # a1 = in1.audio
    # .output('-', format='s16le', acodec='pcm_s16le', ac=1, ar='16k')

    out = ffmpeg.output(in1, outfile, format=file_format).overwrite_output()
    out.run()

def concatenate_video(infile_list, outfile):
    infiles = []
    for filename in infile_list:
        new_infile = ffmpeg.input(filename)
        infiles.append(new_infile)
    joined = ffmpeg.concat(*infiles)
    out = ffmpeg.output(joined, outfile).overwrite_output()
    out.run()
