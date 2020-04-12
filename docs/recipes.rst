Recipes
=======


Downloading from youtube and normalizing volume

function media_download {
    export URL=$1
    youtube-dl \
        -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' \
        --merge-output-format mp4 \
        --no-overwrites \
        --sleep-interval 15 \
        --max-sleep-interval 30 \
        --playlist-start 1 \
        "$URL"
    ~/.local/bin/ffmpeg-normalize *.mkv \
        --progress \
        --output-format mp4 \
        -ext mp4 \
        -c:a aac && \
        mkdir .old && \
        mv *.mkv .old && \
        mv normalized/*.mp4 . && \
        rmdir normalized
}
