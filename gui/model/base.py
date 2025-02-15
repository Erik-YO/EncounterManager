
from pathlib import Path
from tkinter.filedialog import askopenfilename
from typing import Any

from gui.files import IMAGE_FILETYPES, image_dir, search_image


class BaseModel:

    def __init__(self, image_path: Path | str) -> None:
        # Doesn't change if it's absolute
        self.image_path: Path
        self.set_image(image_path)

    def to_dict(self) -> dict[str, Any]:
        return {'img': str(self.get_image_path())}

    @classmethod
    def from_dict(cls, element_data: dict[str, str | int | float]):

        image_path_str = element_data.get('img', None)
        assert image_path_str is not None, (
            'Every element must have an associated image')
        assert isinstance(image_path_str, str)

        bm = super().__new__(cls)
        BaseModel.__init__(bm, image_path_str)
        return bm

    def get_image_path(self) -> Path:
        try:
            return self.image_path.relative_to(image_dir())
        except ValueError:
            return self.image_path

    def set_image(self, new_image: Path | str):
        new_image_path = search_image(new_image)
        while new_image_path is None:
            new_image = askopenfilename(
                initialdir=image_dir(),
                title=(
                    f'Image {new_image} not found, '
                    'please choose a new image'),
                filetypes=(('New image', IMAGE_FILETYPES), )
            )
            new_image_path = search_image(new_image)
        self.image_path: Path = new_image_path
