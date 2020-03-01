Pygame
======

Pygame does not work out of the box on MacOS Mojave.

::

    brew install sdl2 sdl2_gfx sdl2_image sdl2_mixer sdl2_net sdl2_ttf
    pip uninstall pygame
    git clone https://github.com/pygame/pygame.git
    cd pygame
    python setup.py -config -auto -sdl2
    python setup.py install

Minimal player
--------------

::

    from moviepy.editor import VideoFileClip
    import pygame

    FILENAME = 'temp.mp4'

    clip = VideoFileClip(FILENAME)
    # use ESC key to exit
    clip.preview()
    pygame.display.quit()
    pygame.quit()
    clip.close()
