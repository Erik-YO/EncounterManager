
from pygame import Surface

from gui.controller.base import BaseController
from gui.model.background import BackgroundModel
from gui.view.background import BackgroundView


class BackgroundController(BaseController):
    view_class = BackgroundView
    model_class = BackgroundModel

    model: BackgroundModel  # type:ignore

    def render(self, window: Surface):  # type:ignore
        window.blit(self.view.get_surface(), (0, 0))

    def set_scale(self, scale: float):
        if scale == self.model.scale:
            return
        self.model.set_scale(scale)
        self.view.model_updated()
