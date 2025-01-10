
from typing import List, Tuple, Union
from pygame import Surface, init, quit
from pygame import font, display, time, event, draw
from pygame import SRCALPHA

from guitools.const import loadImage, defaultBackground, prepBackground
from guitools.elements import Elemento, Objeto, Aliado, Enemigo
from guitools.userinput import Input


class Loop:

    HELPS = [
        'H - alternar este cuadro',
        'G - alternar la cuadricula',
        'L - (des)bloquear los objetos',
        'Z/Y des/rehacer movimiento',
    ]

    def __init__(
            self,
            windowsize: Tuple[int, int],
            cellSize: float,
            backgroundIcon: Union[str, None] = None,
            objectIcons: List[str] = [],
            playerIcons: List[str] = [],
            monsterIcons: List[str] = [],
            ) -> None:

        self.window: Surface = display.set_mode(windowsize)
        self.clock: time.Clock = time.Clock()
        self.fuente: font.Font = font.SysFont("Consoles", round(cellSize / 2))

        if backgroundIcon is None:
            self.background = defaultBackground(windowsize)
            display.set_caption('Mapa')
        else:
            name = backgroundIcon[:backgroundIcon.find('.')]
            name = name[name.rfind('/') + 1:]
            name = name[name.rfind('\\') + 1:]
            display.set_caption(
                ' '.join(name.split('_')).title())

            self.background = prepBackground(backgroundIcon, windowsize)
        self.elements: List[Elemento] = [
            Aliado(icon, cellSize) for icon in playerIcons
        ] + [
            Enemigo(icon, cellSize) for icon in monsterIcons
        ] + [
            Objeto(icon, cellSize) for icon in objectIcons
        ]
        self.cellSize: float = cellSize

        # Config
        self.locked: bool = False
        self.showGrid: bool = True
        self.showHelp: bool = False
        self.fps: int = 20

        # Input
        self.input = Input()

        # Loopparams
        self.updated: bool = True
        self.running: bool = False
        self.selectedItem: Elemento = None

        # History
        self.history = []
        self.reversehistory = []

    def update(self):
        updated = False

        if self.input.leftclick:
            updated = self.selectItem() or updated
        if self.input.leftunclick:
            updated = self.dropItem() or updated

        if self.input.keyunicode is not None:
            updated = True
            if self.input.keyunicode == 'h':
                self.showHelp = not self.showHelp
            elif self.input.keyunicode == 'g':
                self.showGrid = not self.showGrid
            elif self.input.keyunicode == 'l':
                self.locked = not self.locked
            elif self.input.keyunicode == 'z':
                if self.history:
                    obj, lastpos = self.history.pop()
                    self.reversehistory.append((obj, (obj.posx, obj.posy)))
                    obj.posx, obj.posy = lastpos
            elif self.input.keyunicode == 'y':
                if self.reversehistory:
                    obj, newpos = self.reversehistory.pop()
                    self.history.append((obj, (obj.posx, obj.posy)))
                    obj.posx, obj.posy = newpos
            elif self.input.keyunicode == '':
                ...

        if self.input.leftclicking:
            updated = True

        self.updated = updated

    def show(self):

        if not self.updated:
            return

        self.window.blit(self.background, (0, 0))  # Imagen fondo

        if self.showGrid:  # Grid
            w, h = self.window.get_size()
            x = y = self.cellSize
            white, black = (200, 200, 200), (0, 0, 0)
            while x < w:
                draw.line(self.window, white, (x, 0), (x, h))
                draw.line(self.window, black, (x + 1, 0), (x + 1, h))
                x += self.cellSize
            while y < h:
                draw.line(self.window, white, (0, y), (w, y))
                draw.line(self.window, black, (0, y + 1), (w, y + 1))
                y += self.cellSize

        for elemento in self.elements[::-1]:  # Elementos
            elemento.show(self.window)

        if self.selectedItem is not None:  # Seleccionado
            prev = self.selectedItem.posx, self.selectedItem.posy
            x, y = self.input.mousepos
            x -= self.cellSize / 2
            y -= self.cellSize / 2
            self.selectedItem.posx, self.selectedItem.posy = x, y
            self.selectedItem.show(self.window, True)
            self.selectedItem.posx, self.selectedItem.posy = prev

        if self.showHelp:
            self.help()

        display.update()

        self.updated = False

    def tick(self):
        self.clock.tick(self.fps)

    def mainloop(self):

        while not self.input.quit:
            self.show()
            self.tick()
            self.input.fromEvents(event.get())
            self.update()

        return

    def help(self, _rect: List[Surface] = []):

        if not len(_rect):

            w = h = 0
            for help in Loop.HELPS:
                x, y = self.fuente.size(help)
                h += y
                w = max(w, x)

            w += 4
            h += 4
            surf = Surface((w, h), SRCALPHA)
            surf.fill((250, 250, 250, 150))
            _rect.append(surf)

            x = y = 2
            for help in Loop.HELPS:
                line = self.fuente.render(help, True, (0, 0, 0))
                surf.blit(line, (x, y))
                y += line.get_height()

        self.window.blit(
            _rect[0],
            (self.window.get_width() - _rect[0].get_width(), 0))

        return

    def selectItem(self) -> bool:

        prev = self.selectedItem
        if prev is not None:
            self.dropItem()

        x, y = self.input.mousepos
        for item in self.elements:
            if item.lockable and self.locked:
                continue
            if item.inside(x, y):
                self.selectedItem = item
                break

        return self.selectedItem is not prev

    def dropItem(self) -> bool:

        if self.selectedItem is None:
            return False

        self.elements.pop(self.elements.index(self.selectedItem))
        self.elements.insert(0, self.selectedItem)

        x, y = self.input.mousepos
        newx = (x // self.cellSize) * self.cellSize
        newy = (y // self.cellSize) * self.cellSize

        if x != newx or y != newy:
            self.history.append((
                self.selectedItem,
                (self.selectedItem.posx, self.selectedItem.posy)))
            self.reversehistory.clear()

        self.selectedItem.posx = newx
        self.selectedItem.posy = newy

        self.selectedItem = None
        return True


def loop(
        windowsize: Tuple[int, int],
        minNCells: float,
        backgroundIcon: Union[None, str],
        objectIcons: List[str],
        playerIcons: List[str],
        monsterIcons: List[str],
        fullImage: bool = False):

    # Inicializacion de pygame
    init()
    font.init()

    if fullImage:

        if backgroundIcon is None:
            raise ValueError(
                'Para usar la opcion fullImage debe haber '
                'un background valido')

        bg = loadImage(backgroundIcon)
        maxw, maxh = windowsize
        x, y = bg.get_size()

        if x / y > maxw / maxh:
            maxh = maxw * y / x
        else:
            maxw = maxh * x / y

        windowsize = (maxw, maxh)

    w, h = windowsize
    if w < h:
        cellsize = w / minNCells
    else:
        cellsize = h / minNCells

    loopobj = Loop(
        windowsize, cellsize, backgroundIcon,
        objectIcons, playerIcons, monsterIcons)

    loopobj.mainloop()

    display.quit()
    quit()


if __name__ == '__main__':
    from guitools.loader import paramsFromFile
    from guitools.menu import Menu
    from os.path import exists, isfile, dirname

    # Ultima carpeta usada
    lastfolder_reg = '.lastdir'
    folder = None
    if exists(lastfolder_reg) and isfile(lastfolder_reg):
        with open(lastfolder_reg, 'r') as f:
            folder = f.read()
        if not folder or not exists(folder):
            folder = None

    menu = Menu(folderPath=folder)
    file, new = menu.loop()
    if file is None and not new:
        exit()

    print(file, new, menu.currentFolder)
    if new or not file:
        exit()

    # Ultima carpeta usada
    with open(lastfolder_reg, 'w') as f:
        f.write(dirname(file))

    print(file)
    params = paramsFromFile(file)
    loop(*params)
