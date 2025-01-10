from typing import Tuple, Iterable
from pygame import (
    event, key, mouse,
    QUIT, KEYDOWN, MOUSEWHEEL, MOUSEBUTTONDOWN, MOUSEBUTTONUP)


class Input:

    def __init__(self):
        self.clicking: Tuple[bool, bool] = (False, False)
        self.old_clicking: Tuple[bool, bool] = self.clicking

        self.click: Tuple[bool, bool] = (False, False)
        self.unclick: Tuple[bool, bool] = (False, False)

        self.old_click: Tuple[bool, bool] = self.click
        self.old_unclick: Tuple[bool, bool] = self.unclick

        self.keypressed: Tuple[str, str, str] = ('', '', '')
        self.old_keypressed: Tuple[str, str, str] = self.keypressed

        self.mousepos: Tuple[int, int] = (0, 0)
        self.old_mousepos: Tuple[int, int] = self.mousepos

        self.wheel: Tuple[int, int] = (0, 0)
        self.old_wheel: Tuple[int, int] = (0, 0)

        self.quit: bool = False

    def update(
            self, click: Tuple[bool, bool],
            unclick: Tuple[bool, bool],
            clicking: Tuple[bool, bool],
            mousePos: Tuple[int, int],
            wheel: Tuple[int, int],
            keyPressed: Tuple[str, str, str],
            quit: bool):

        self.old_clicking = self.clicking
        self.old_click = self.click
        self.old_unclick = self.unclick
        self.old_keypressed = self.keypressed
        self.old_mousepos = self.mousepos
        self.old_wheel = wheel

        self.clicking = clicking
        self.click = click
        self.unclick = unclick
        self.keypressed = keyPressed
        self.mousepos = mousePos
        self.wheel = wheel

        self.quit = quit

    def fromEvents(self, events: Iterable[event.Event]):

        key_pressed = ('', '', '')
        quit = False
        wheel = (0, 0)
        click = [False, False]
        unclick = [False, False]
        clicking = mouse.get_pressed()
        clicking = (clicking[0], clicking[2])

        for evento in events:

            if evento.type == QUIT:
                quit = True

            elif evento.type == KEYDOWN:
                key_pressed = key.name(evento.key)
                try:
                    key_pressed = (
                        key_pressed, evento.unicode,
                        key.key_code(key_pressed))
                except ValueError:
                    key_pressed = key_pressed, evento.unicode, None

            elif evento.type == MOUSEWHEEL:
                wheel = (evento.x, evento.y)

            elif evento.type == MOUSEBUTTONDOWN:
                click[0] = clicking[0]
                click[1] = clicking[1]

            elif evento.type == MOUSEBUTTONUP:
                unclick[0] = not clicking[0]
                unclick[1] = not clicking[1]

        pos = mouse.get_pos()

        self.update(
            tuple(click), tuple(unclick), clicking,
            pos, wheel, key_pressed, quit)

    @property
    def wheelx(self):
        return self.wheel[0]

    @property
    def wheely(self):
        return self.wheel[1]

    @property
    def mousex(self):
        return self.mousepos[0]

    @property
    def mousey(self):
        return self.mousepos[1]

    @property
    def mousemoved(self):
        return self.mousepos != self.old_mousepos

    @property
    def leftunclick(self):
        return self.unclick[0]

    @property
    def rightunclick(self):
        return self.unclick[1]

    @property
    def leftclick(self):
        return self.click[0]

    @property
    def rightclick(self):
        return self.click[1]

    @property
    def leftclicking(self):
        return self.clicking[0]

    @property
    def rightclicking(self):
        return self.clicking[1]

    @property
    def keyname(self):
        return self.keypressed[0]

    @property
    def keyunicode(self):
        return self.keypressed[1]

    @property
    def keycode(self):
        return self.keypressed[2]

    def __str__(self) -> str:
        return f'{self.__class__.__name__}{vars(self)}'

    def __repr__(self) -> str:
        return str(self)
