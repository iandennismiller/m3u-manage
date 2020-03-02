# m3u-manage

## Milestone 4: video management

- [x] side-by-side IN.M3U OUT.M3U: using ffmpeg, convert all videos to sbs projection
- [ ] repack IN.M3U mp4: using ffmpeg, convert all files in .m3u to specified format
- [ ] combine --fade IN.M3U OUT.MP4: using ffmpeg, concatenate all files into specified file
- [ ] volume-normal IN.M3U: using ffmpeg, normalize the volume of all files in playlist

## Milestone 5: transmission

- [ ] cast IN.M3U DESTINATION_CHROMECAST: using VLC, stream playlist to device
- [ ] stream IN.M3U rtsp,http: stream playlist with VLC over protocol
- [ ] upcoming IN.M3U OUT.MP4: using ffmpeg, generate video with overview of m3u contents

## Milestone 6: interaction

- [ ] page IN.M3U: render a web page for watching videos in m3u
- [ ] site CONFIG.JSON: render tube-like website based on config
- [ ] serve IN.M3U: run a simple http server to publish results of page/site
- [ ] integrate tags into server

## Done

### Milestone 1: project setup

- [x] create project: project-new m3u-manage
- [x] scaffold project: diamond --skel python scaffold
- [x] create repository at https://github.com/new
    + [x] set description
    + [x] set documentation website
- [x] enable continuous integration at https://travis-ci.org/profile/
- [x] enable documentation at https://readthedocs.org/dashboard/import/
    + [x] admin -- advanced settings -- requirements file -- ".readthedocs.txt"
- [x] pypi (python setup.py register -r https://pypi.python.org/pypi)
- [x] release to pypi (make release)
- [x] install development environment (make dev test)
- [x] install production environment

### Milestone 2: file management

- [x] analyze PATH tags.json: update syntax to just take a path, ignoring tags
- [x] regularize PATH: for all files in PATH, tolower filenames, fix garbage in filenames
- [x] gather FROM_PATH TO_PATH: recursively move from_path into to_path, flattening directory hierarchy
- [x] decide PATH DEST1 DEST2: for all files in PATH, preview each and sort into DEST1 or DEST2 with a single keypress, then automatically advance
- [x] tag PATH tags.json: for all files in PATH, preview and single-keypress interface to add tags, from tags.json, to filenames (i.e. append strings)

## Milestone 3: list management

- [x] repeat OUT.M3U VIDEO N-TIMES: create playlist consisting of video repeated
- [x] append IN.M3U VIDEO: update m3u by appending video to end
- [x] insert IN.M3U INDEX VIDEO: update m3u by inserting video at specified index (0 for start)
- [x] delete IN.M3U INDEX: update m3u by deleting video at specified index
- [x] get IN.M3U INDEX: print video at specified index
- [x] summary IN.M3U: print summary of m3u, with titles and durations
