

from pygame import (
    event, key, mouse,
    QUIT, KEYDOWN,
    MOUSEWHEEL, MOUSEBUTTONDOWN, MOUSEBUTTONUP,
    DROPFILE)


class UserInput:

    def __init__(self):
        self.clicking: tuple[bool, bool] = (False, False)
        self.old_clicking: tuple[bool, bool] = self.clicking

        self.click: tuple[bool, bool] = (False, False)
        self.unclick: tuple[bool, bool] = (False, False)

        self.old_click: tuple[bool, bool] = self.click
        self.old_unclick: tuple[bool, bool] = self.unclick

        self.keypressed: tuple[str, str, str] = ('', '', '')
        self.old_keypressed: tuple[str, str, str] = self.keypressed

        self.mousepos: tuple[int, int] = (0, 0)
        self.old_mousepos: tuple[int, int] = self.mousepos

        self.wheel: tuple[int, int] = (0, 0)
        self.old_wheel: tuple[int, int] = (0, 0)

        self.drop_file: str | None = None
        self.old_drop_file: str | None = None

        self.quit: bool = False

    def update(
            self,
            click: tuple[bool, bool],
            unclick: tuple[bool, bool],
            clicking: tuple[bool, bool],
            mousePos: tuple[int, int],
            wheel: tuple[int, int],
            keyPressed: tuple[str, str, str],
            drop_file: str | None,
            quit: bool):

        self.old_clicking = self.clicking
        self.old_click = self.click
        self.old_unclick = self.unclick
        self.old_keypressed = self.keypressed
        self.old_mousepos = self.mousepos
        self.old_wheel = self.wheel
        self.old_drop_file = self.drop_file

        self.clicking = clicking
        self.click = click
        self.unclick = unclick
        self.keypressed = keyPressed
        self.mousepos = mousePos
        self.wheel = wheel
        self.drop_file = drop_file

        self.quit = quit

    def fromEvents(self, events: list[event.Event]):

        key_pressed = ('', '', '')
        quit = False
        wheel = (0, 0)
        click = [False, False]
        unclick = [False, False]
        clicking = mouse.get_pressed()
        clicking = (clicking[0], clicking[2])
        drop_file: str | None = None

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

            elif evento.type == DROPFILE:
                drop_file = evento.file

        pos = mouse.get_pos()

        self.update(
            tuple(click), tuple(unclick), clicking,  # type:ignore
            pos, wheel, key_pressed, drop_file, quit)  # type:ignore

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
        return f'{type(self).__name__}{vars(self)}'

    def __repr__(self) -> str:
        return str(self)
