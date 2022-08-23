import os
import pygame as pg
from pygame.rect import Rect
from pygame.surface import Surface

from services.constants import Folders


def load_image(name: str,
               colorkey=None,
               scale=1) -> tuple[Surface, Rect]:

    fullname = os.path.join(os.path.abspath(os.curdir),
                            Folders.Static.value,
                            name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)

    return image, image.get_rect()

