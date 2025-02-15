
from pathlib import Path
from tkinter.messagebox import showerror

ENCOUNTER_FILETYPES = '*.json'
IMAGE_FILETYPES = '*.png *.jpg *.jpeg *.gif *.webp *.ico'


def base_dir() -> Path:
    bp = Path('~/.encountermanager').expanduser()
    if not bp.is_dir():
        if bp.exists():
            ttl = ''
            msg = ''
            showerror(ttl, msg)
            raise FileExistsError(f'{ttl}: {msg}')
        bp.mkdir()

    return bp


def image_dir() -> Path:
    ip = base_dir().joinpath('images')
    ip.mkdir(parents=True, exist_ok=True)
    return ip


def encounter_dir() -> Path:
    ep = base_dir().joinpath('encounters')
    ep.mkdir(parents=True, exist_ok=True)
    return ep


def search_image(original_path: Path | str) -> Path | None:
    original_path = image_dir().joinpath(original_path)

    if original_path.is_file():
        try:
            return original_path.relative_to(image_dir())
        except ValueError:
            return original_path

    # DFS
    original_name = original_path.name

    path_stack = list(base_dir().iterdir())
    try:
        # We look first in the images directory
        img_idx = path_stack.index(image_dir())
        path_stack.append(path_stack.pop(img_idx))
    except ValueError:
        ...

    while len(path_stack):
        current = path_stack.pop()

        if current.is_dir():
            path_stack.extend(current.iterdir())

        elif current.is_file():
            if current.name == original_name:
                try:
                    return current.relative_to(image_dir())
                except ValueError:
                    return current

    return None


if __name__ == '__main__':
    print(f'{base_dir()=}')
    print(f'{image_dir()=}')
    print(f'{encounter_dir()=}')

    img = 'Ghast.webp'
    found = search_image(img)
    print(f'{img} -> {found}')
