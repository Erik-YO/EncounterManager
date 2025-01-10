
from typing import Dict, Tuple, Union
from os.path import abspath, join, isfile
from pygame import Surface, BLEND_RGBA_MULT
from pygame import image
from pygame import transform
from pygame import SRCALPHA
from pygame import mask as mk
from pygame import draw


IMGS_DIR = 'imgs'
DEFAULT_FOLDER = 'encounters'
DEFAULT_FOLDER_PATH = abspath(join(__file__, DEFAULT_FOLDER))
RESOURCEPATH = abspath(join(__file__, IMGS_DIR))
DEFAULTCOLOR = (211, 155, 108)


def loadImage(filename: str, absolute: bool = True) -> Surface:
    if not filename:
        return None

    name = filename
    if not absolute:
        filename = join(RESOURCEPATH, filename)
    filename = abspath(filename)

    if not isfile(filename):
        raise ValueError(f'Imagen "{name}" no existe')

    return image.load(filename)


def defaultBackground(
        size: Tuple[int, int],
        _bg: Dict[Tuple[int, int], Surface] = dict()) -> Surface:

    bg = _bg.get(size)
    if bg is not None:
        return bg

    bg = Surface(size, SRCALPHA)
    bg.fill(DEFAULTCOLOR)

    _bg[size] = bg

    return bg


def fitImg(
        img: Surface,
        newSize: Tuple[int, int],
        middleCrop: bool = True) -> Surface:

    x, y = img.get_size()
    if (x, y) == newSize:
        return img

    p = y / x
    nx, ny = newSize
    np = ny / nx

    if p > np:
        factor = nx / x
        img = transform.smoothscale(img, (nx, y * factor))

    else:
        factor = ny / y
        img = transform.smoothscale(img, (x * factor, ny))

    left = top = 0

    if img.get_width() > nx:
        left = (img.get_width() - nx) / 2 if middleCrop else 0

    if img.get_height() > ny:
        top = (img.get_height() - ny) / 2 if middleCrop else 0

    new = Surface((nx, ny), SRCALPHA)
    new.blit(img, (0, 0), (left, top, nx, ny))

    return new


def prepImage(
        image: Surface, size: float,
        circular: Union[None, Tuple[int, int, int]], *,
        _masks: Dict[float, mk.Mask] = dict()) -> Surface:

    image = fitImg(image, (size, size), False)

    if circular is not None:
        mask = _masks.get(size)
        if mask is None:

            circle = Surface((size, size), SRCALPHA)
            circle.fill((0, 0, 0, 0))
            draw.circle(
                circle, (255, 255, 255),
                (size / 2, size / 2), size / 2)
            mask = circle  # mk.from_surface(circle)

            _masks[size] = mask

        newimg = mask.copy()
        newimg.blit(image, (0, 0), None, BLEND_RGBA_MULT)
        image = newimg

    return image


def prepBackground(image: str, windowSize: Tuple[int, int]):
    if not image:
        return defaultBackground(windowSize)
    return fitImg(loadImage(image), windowSize)


def scaleLimit(
        image: Surface, maxdims: Union[Tuple[int, int], int]
        ) -> Surface:
    if isinstance(maxdims, int):
        maxdims = (maxdims, maxdims)

    maxx, maxy = maxdims
    sx, sy = image.get_size()

    mf = maxx / maxy
    sf = sx / sy

    if mf > sf:
        factor = maxy / sy
    else:
        factor = maxx / sx

    newsize = (sx * factor, sy * factor)

    new = Surface(newsize, SRCALPHA)
    img = transform.smoothscale(image, newsize)
    new.blit(img, (0, 0))
    return new
