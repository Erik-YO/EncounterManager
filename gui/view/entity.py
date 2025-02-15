

from pygame import Surface

from gui.values import ImageShape
from gui.utils.image import ImageUtils
from gui.model.entity import EntityModel
from gui.view.base import BaseView


class EntityView(BaseView):
    _model: EntityModel

    def __init__(self, model: EntityModel, base_size: float) -> None:
        super().__init__(model)
        self._base_size = base_size

    def get_base_size(self) -> float:
        return self._base_size

    def set_base_size(self, base_size: float):
        if base_size != self._base_size:
            self._base_size = base_size
            self._surface = None

    def draw_surface(self) -> Surface:
        cellsize = self._base_size * self._model.size
        surf = ImageUtils.fit(
            ImageUtils.load(self._model.image_path),
            (cellsize, cellsize), True)

        match self._model.shape:
            case ImageShape.ORIGINAL:
                surface = surf
            case ImageShape.CIRCULAR:
                surface = ImageUtils.circular_crop(surf, cellsize)
            case _:
                raise ValueError(
                    f'Shape "{self._model.shape.value}" not supported')

        return surface
