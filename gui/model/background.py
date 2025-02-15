
from typing import Any
from gui.model.base import BaseModel


class BackgroundModel(BaseModel):
    scale = 1.0

    def __init__(self, scale: float) -> None:
        self.scale = scale

    def to_dict(self) -> dict[str, Any]:
        return super().to_dict() | ({
            'scale': self.scale
        } if self.scale != BackgroundModel.scale else {})

    @classmethod
    def from_dict(cls, element_data: dict[str, str | int | float]):
        scale = element_data.get('scale', cls.scale)
        assert isinstance(scale, (float, int)), (
            'The background "scale" must be a number')
        assert scale > 0, 'The background scale must be bigger than 0'

        bg = super().from_dict(element_data)
        BackgroundModel.__init__(bg, float(scale))
        return bg

    def set_scale(self, scale: float):
        self.scale = scale
