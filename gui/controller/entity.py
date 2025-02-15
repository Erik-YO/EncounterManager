
from pygame import Surface

from gui.controller.base import BaseController
from gui.model.entity import EntityModel
from gui.values import ImageShape
from gui.view.entity import EntityView


class EntityController(BaseController):
    view_class = EntityView
    model_class = EntityModel

    view: EntityView  # type:ignore
    model: EntityModel  # type:ignore

    @classmethod
    def from_dict(
            cls, element_data: dict[str, int | float | str],
            base_size: float | None = None):

        model = cls.model_class.from_dict(element_data)
        view = cls.view_class(
            model,
            cls.view_class.DEFAULT_BASE_SIZE
            if base_size is None else base_size)

        ec = super().__new__(cls)
        EntityController.__init__(ec, model, view)
        return ec

    def render(self, window: Surface, cell_size: float):
        image = self.view.get_surface()

        # position calculations depending on size_category y cell_size
        x, y = self.model.x * cell_size, self.model.y * cell_size
        if self.model.size < 1:
            prop = cell_size * self.model.size / 2
            x += prop
            y += prop

        window.blit(image, (x, y))

    def is_hovering(self, x: int, y: int, cell_size: float) -> bool:

        minx = self.model.x * cell_size
        miny = self.model.y * cell_size
        size = cell_size * self.model.size
        if self.model.size < 1:
            prop = size / 2
            minx += prop
            miny += prop

        hor = (x > minx) and (x < (minx + size))
        ver = (y > miny) and (y < (miny + size))
        return hor and ver

    # Model modifications

    def grow(self):
        self.model.grow()
        self.view.model_updated()

    def shrink(self):
        self.model.shrink()
        self.view.model_updated()

    def move(self, x: int, y: int):
        self.model.move(x, y)

    def change_shape(self):
        new = self.model.shape.next()
        assert isinstance(new, ImageShape)
        self.model.set_shape(new)
        self.view.model_updated()

    # View modifications

    def change_cell_size(self, new_cell_size: float):
        self.view.set_base_size(new_cell_size)
        self.view.model_updated()
