
from pygame import Surface
from gui.model.base import BaseModel
from gui.utils.image import ImageUtils
from gui.model.background import BackgroundModel
from gui.view.base import BaseView


class BackgroundView(BaseView):
    _model: BackgroundModel

    def draw_surface(self) -> Surface:
        surf = super().draw_surface()
        surf = ImageUtils.scale(surf, self._model.scale)
        return surf
