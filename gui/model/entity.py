
from typing import Any
from gui.model.base import BaseModel
from gui.values import ImageShape


class EntityModel(BaseModel):
    x = 0
    y = 0
    size = 1
    shape = ImageShape.ORIGINAL

    def __init__(
            self, x: int, y: int, size: int | float, shape: ImageShape
            ) -> None:
        self.x = x
        self.y = y
        self.size = size
        self.shape = shape

    def to_dict(self) -> dict[str, Any]:
        default_pos = (self.__class__.x, self.__class__.y)
        return super().to_dict() | ({
            'x': self.x,
            'y': self.y,
        } if (self.x, self.y) != default_pos else {}) | ({
            'size': self.size
        } if self.size != self.__class__.size else {}) | ({
            'shape': self.shape.value,
        } if self.shape != self.__class__.shape else {})

    @classmethod
    def from_dict(
            cls, element_data: dict[str, str | int | float]
            ):

        posx = element_data.get('x', cls.x)
        posy = element_data.get('y', cls.y)
        assert isinstance(posx, int) and isinstance(posy, int), (
            'Positions "x" and "y" must be integers')

        size = element_data.get('size', cls.size)
        assert isinstance(size, (int, float)), (
            'The size category "size" must be a number')

        shape = element_data.get('shape', cls.shape.value)
        assert ImageShape.has_value(shape), (
            'The image shape must be one of the supported '
            f'options {tuple(s.value for s in ImageShape)}, not {repr(shape)}')
        shape = ImageShape(shape)

        bm = super().from_dict(element_data)
        EntityModel.__init__(bm, posx, posy, size, shape)
        return bm

    # Modifications

    def move(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y

    def grow(self):
        if self.size < 1:
            self.size *= 2
        else:
            self.size += 1

    def shrink(self):
        if self.size <= 1:
            self.size /= 2
        else:
            self.size -= 1

    def set_shape(self, new_shape: ImageShape):
        self.shape = new_shape
