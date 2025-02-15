
from pathlib import Path

import pygame as pg
from pygame import Surface

from gui.files import image_dir


class ImageUtils:
    _cache: dict[Path, Surface] = dict()
    _circular_masks: dict[float, Surface] = dict()

    @staticmethod
    def _get_circular_mask(diameter: float) -> Surface:
        _cached = ImageUtils._circular_masks.get(diameter)
        if _cached is not None:
            return _cached.copy()

        mask = Surface((diameter, diameter), pg.SRCALPHA)
        mask.fill((0, 0, 0, 0))
        pg.draw.circle(
            mask, (255, 255, 255),
            (diameter / 2, diameter / 2), diameter / 2)

        ImageUtils._circular_masks[diameter] = mask
        return mask.copy()

    @staticmethod
    def load(image_path: Path) -> Surface:
        image_path = image_dir().joinpath(image_path)
        _cached = ImageUtils._cache.get(image_path)
        if _cached is not None:
            return _cached

        assert isinstance(image_path, Path)
        assert image_path.is_file(), f'Image path "{image_path}" not found'

        img = pg.image.load(image_path).convert()

        return img

    @staticmethod
    def fit(
            image: Surface, new_size: tuple[float, float],
            symetric_crop: bool = True) -> Surface:
        cx, cy = image.get_size()
        if (cx, cy) == new_size:
            return image

        incline = cy / cx
        nx, ny = new_size
        new_incline = ny / nx

        if incline > new_incline:
            factor = nx / cx
            transformed = pg.transform.smoothscale(
                image.convert_alpha(), (nx, cy * factor))
        else:
            factor = ny / cy
            transformed = pg.transform.smoothscale(
                image.convert_alpha(), (cx * factor, ny))

        left = top = 0

        if transformed.get_width() > nx:
            left = (nx - transformed.get_width()) / 2 if symetric_crop else 0
        if transformed.get_height() > ny:
            top = (ny - transformed.get_height()) / 2 if symetric_crop else 0

        surf = Surface((nx, ny), transformed.get_flags())
        surf.blit(transformed, (left, top, nx, ny))
        return surf

    @staticmethod
    def circular_crop(image: Surface, diameter: float) -> Surface:
        mask = ImageUtils._get_circular_mask(diameter)
        mask.blit(image, (0, 0), None, pg.BLEND_RGBA_MULT)
        return mask

    @staticmethod
    def limited_scale(
            image: Surface, maxdims: tuple[int, int] | int) -> Surface:
        if isinstance(maxdims, int):
            maxx = maxy = maxdims
        else:
            maxx, maxy = maxdims

        cx, cy = image.get_size()

        new_incline = maxx / maxy
        incline = cx / cy

        factor = (maxy / cy) if new_incline > incline else (maxx / cx)
        newsize = (cx * factor, cy * factor)

        surf = Surface(newsize, pg.BLEND_RGB_MULT)
        surf.blit(pg.transform.smoothscale(image, newsize), (0, 0))
        return surf

    @staticmethod
    def scale(image: Surface, factor: float) -> Surface:
        assert factor > 0

        newsize = (
            round(factor * image.get_width()),
            round(factor * image.get_height()))

        surf = Surface(newsize, pg.BLEND_RGB_MULT)
        surf.blit(pg.transform.smoothscale(image, newsize), (0, 0))
        return surf
