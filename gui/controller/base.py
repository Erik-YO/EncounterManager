
from pathlib import Path
from pygame import Surface

from gui.model.base import BaseModel
from gui.view.base import BaseView


class BaseController:
    view_class = BaseView
    model_class = BaseModel

    view: BaseView
    model: BaseModel

    def __init__(self, model: BaseModel, view: BaseView) -> None:
        self.model = model
        self.view = view

    @classmethod
    def from_dict(
            cls, element_data: dict[str, int | float | str]):

        model = cls.model_class.from_dict(element_data)
        view = cls.view_class(model)

        ec = super().__new__(cls)
        BaseController.__init__(ec, model, view)
        return ec

    def render(self, window: Surface, cell_size: float):
        raise NotImplementedError()

    # Modifications

    def change_image(self, new_image: Path):
        self.model.set_image(new_image)
        self.view.model_updated()
