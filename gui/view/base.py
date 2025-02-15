
from pygame import Surface

from gui.utils.image import ImageUtils
from gui.model.base import BaseModel


class BaseView:
    DEFAULT_BASE_SIZE = 100

    def __init__(self, model: BaseModel) -> None:
        self._model = model
        self._surface: Surface | None = None

    def model_updated(self):
        self._surface = None

    def get_surface(self) -> Surface:
        if self._surface is None:
            self._surface = self.draw_surface()
        return self._surface

    def draw_surface(self) -> Surface:
        return ImageUtils.load(self._model.image_path)

    @classmethod
    def from_model(cls, model: BaseModel):
        ev = super().__new__(cls)
        BaseView.__init__(ev, model)
        return ev
