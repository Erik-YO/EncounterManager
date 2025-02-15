
# from tkinter.filedialog import askopenfile, askopenfilename, asksaveasfilename
# from tkinter.messagebox import askquestion, askokcancel, askyesno, askyesnocancel, askretrycancel

import os
from tkinter.filedialog import askopenfilename, asksaveasfilename

import json
from pathlib import Path

from gui.files import ENCOUNTER_FILETYPES, IMAGE_FILETYPES, base_dir, encounter_dir
from gui.screen import Screen


def prepare_window_pos():
    x, y = 50, 50
    os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'


def main():

    file = askopenfilename(
        title='Choose an encounter file or a background image',
        initialdir=base_dir(),
        filetypes=(
            ('Encounter', ENCOUNTER_FILETYPES),
            ('Background image', IMAGE_FILETYPES),
        ))
    if not file:
        return
    file = Path(file)

    prepare_window_pos()
    Screen.init()
    from_encounter = file.suffix in ENCOUNTER_FILETYPES or not file.suffix

    if from_encounter:
        with file.open('r') as f:
            string = f.read()
        data = json.loads(string)
        screen = Screen.from_dict(data)
    else:
        screen = Screen.from_image(file)

    print(screen.encounter.to_dict())
    try:
        screen.loop()
    finally:
        Screen.close()

    datas = json.dumps(screen.encounter.to_dict())
    print(datas)
    MAX_ITERATIONS = 10
    for _ in range(MAX_ITERATIONS):
        if from_encounter:
            save_as = asksaveasfilename(
                title='Save as',
                filetypes=(('Encounter', ENCOUNTER_FILETYPES), ),
                initialfile=file.name,
                initialdir=file.parent,
            )
        else:
            save_as = asksaveasfilename(
                title='Save as',
                filetypes=(('Encounter', ENCOUNTER_FILETYPES), ),
                initialdir=encounter_dir(),
            )
        if save_as:
            save_as = Path(save_as).with_suffix('.json')
            with save_as.open('w') as f:
                f.write(datas)
        break


if __name__ == '__main__':
    main()
