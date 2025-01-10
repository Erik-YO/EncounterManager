
from typing import List, Union, Tuple
import pygame as pg
from tkinter.filedialog import askopenfilename, asksaveasfilename
from json import dump, load
from os.path import abspath, dirname, join, basename

from guitools.userinput import Input
from guitools.elements import Aliado, Enemigo, Objeto, Elemento
from guitools.const import (
    defaultBackground, prepBackground,
    loadImage, scaleLimit, RESOURCEPATH)


class Creator:

    HELP = [
        'H : Show/hide this help message',
        'G : Show/hide grid',
        '',
        'B : Choose new background',
        '+ / - : Bigger/Smaller grid',
        'W / W+Shift : More/Less max width',
        'T / T+Shift : More/Less max tallness',
        'R : Change type of element',
        'A : Add object',
        'S / S+Shift : Bigger/Smaller size category of element',
        # 'Z/Y : Undo/redo element movement',
        'Esc - close or unselect element',
    ]

    SCREEN_SIZE: Tuple[int, int] = (200, 100)
    WSIZE: Tuple[int, int] = (300, 300)
    DEFCOLOR: Tuple[int, int, int] = (211, 155, 108)
    SIZE_INCREMENT: int = 1.1

    elementos: List[Elemento]
    grid: int
    filename: Union[None, str]
    quit: bool
    selected: Union[None, Elemento]
    movingSelected: bool

    window: pg.Surface
    fuente: pg.font.Font
    background: pg.Surface
    backgroundfile: Union[None, str]
    tickN: int

    def __init__(self) -> None:
        ...

    # Startup & end methods

    def reset(self):
        self.elementos = []
        self.filename = None
        self.input = Input()
        self.backgroundfile = None
        self.grid = 1  # Min = 1
        self.selected = None
        self.visibleHelp = False
        self.visibleGrid = True
        self.movingSelected = False
        self.originalSize = (0, 0)
        # History
        self.history = []
        self.reversehistory = []
        self.tickN = 0

        pg.init()
        pg.font.init()
        pg.display.set_caption('Encounter creator')

        win = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        Creator.SCREEN_SIZE = win.get_size()

        self.resize(Creator.WSIZE)

    def close(self):
        pg.font.quit()
        pg.quit()

    # Loop

    def creationLoop(self):
        clock = pg.time.Clock()
        while not self.input.quit:

            # Show
            self.show()
            clock.tick(20)

            # Input
            self.input.fromEvents(pg.event.get())

            # Update
            self.update()
            self.tickN += 1

        return

    # Dump to file

    def dump(self, folderpath):
        if self.filename is None:
            self.filename = asksaveasfilename(
                title='Guardar como',
                initialdir=folderpath,
                filetypes=(
                    ("JSON", "*.json"),
                    ("Config", "*.config")))
        else:
            self.filename = asksaveasfilename(
                title='Guardar como',
                initialdir=folderpath,
                initialfile=basename(self.filename),
                filetypes=(
                    ("JSON", "*.json"),
                    ("Config", "*.config")))

        if not self.filename:
            self.filename = None
            return

        if self.filename.endswith('.json'):
            self.dumpJson()
        elif self.filename.endswith('.config'):
            self.dumpConfig()
        else:  # Default JSON
            self.filename += '.json'
            self.dumpJson()

    def dumpJson(self):

        data = {
            "maxw": self.window.get_width(),
            "maxh": self.window.get_height(),
            "mincells": self.grid,
            "background": self.backgroundfile,

            "object": [
                e.data() for e in self.elementos if e.__class__ is Objeto
            ],

            "player": [
                e.data() for e in self.elementos if e.__class__ is Aliado
            ],

            "mob": [
                e.data() for e in self.elementos if e.__class__ is Enemigo
            ],

            "fullImage": self.originalSize == self.window.get_size()
        }

        print('\n', data, '\n')
        with open(self.filename, 'w') as f:
            dump(data, f)

        return

    def dumpConfig(self):
        raise NotImplementedError()

    # Main method

    def createFromJSON(self, filepath: str) -> Union[str, None]:

        self.reset()

        self.filename = abspath(join(
            dirname(__file__), filepath))

        with open(self.filename, 'r') as f:
            data: dict = load(f)

        self.grid = data.get("mincells")
        w, h = data.get('maxw'), data.get('maxh')
        if w and h:
            self.resize((w, h))

        self.backgroundfile = data.get('background')
        if not data.get('fullImage'):
            self.background = scaleLimit(
                loadImage(self.backgroundfile),
                self.window.get_size())
        else:
            self.background = prepBackground(
                self.backgroundfile,
                self.window.get_size())
        self.originalSize = self.background.get_size()

        self.elementos = [
            Objeto(o, self.cellsize) for o in data.get('object', [])
        ] + [
            Enemigo(e, self.cellsize) for e in data.get('mob', [])
        ] + [
            Aliado(a, self.cellsize) for a in data.get('player', [])
        ]

        # Creation Loop
        self.creationLoop()

        self.dump(dirname(self.filename))

        self.close()

        return self.filename

    def create(self, folderpath: str) -> Union[str, None]:
        self.reset()

        # Creation Loop
        self.creationLoop()

        self.dump(folderpath)

        self.close()
        return self.filename

    # Methods

    def resize(self, wsize: Tuple[int, int]):
        self.window = pg.display.set_mode(wsize)
        fontPixelHeight = 26
        self.fuente = pg.font.SysFont('Roboto', fontPixelHeight)

        if self.backgroundfile:
            self.background = prepBackground(self.backgroundfile, wsize)
        else:
            self.background = defaultBackground(wsize)

        newcs = self.cellsize
        for elemento in self.elementos:
            elemento.resize(newcs)

        self.updated = True

    def chooseBackground(self):
        if self.backgroundfile:
            file = askopenfilename(
                title='Elegir fondo',
                initialfile=self.backgroundfile,
                initialdir=dirname(self.backgroundfile))
        else:
            file = askopenfilename(
                title='Elegir fondo')

        file = file if file else None
        if not file:
            return
        self.backgroundfile = file
        self.background = scaleLimit(
            loadImage(self.backgroundfile),
            (n * 3 // 4 for n in Creator.SCREEN_SIZE))
        self.originalSize = self.background.get_size()
        self.window = pg.display.set_mode(self.originalSize)
        self.updated = True

    def showgrid(self):
        if not self.grid:
            return

        w, h = self.window.get_size()
        x = y = self.cellsize
        white, black = (200, 200, 200), (0, 0, 0)
        while x < w:
            pg.draw.line(self.window, white, (x, 0), (x, h))
            pg.draw.line(self.window, black, (x + 1, 0), (x + 1, h))
            x += self.cellsize
        while y < h:
            pg.draw.line(self.window, white, (0, y), (w, y))
            pg.draw.line(self.window, black, (0, y + 1), (w, y + 1))
            y += self.cellsize

    def showhelp(self):
        ow, oh = self.window.get_size()
        w = ow * 3 / 4
        h = oh * 3 / 4

        surf = pg.Surface((w, h), pg.SRCALPHA)
        surf.fill((250, 250, 250, 150))

        x = y = 2
        for help in Creator.HELP:
            line = self.fuente.render(help, True, (0, 0, 0))
            surf.blit(line, (x, y))
            y += line.get_height()

        self.window.blit(surf, ((ow - w) / 2, (oh - h) / 2))

    @property
    def cellsize(self):
        return min(self.window.get_size()) / self.grid

    def smallerGrid(self):
        self.grid += 1
        self.updated = True

        newcs = self.cellsize
        for elemento in self.elementos:
            elemento.resize(newcs)

    def biggerGrid(self):
        if self.grid <= 1:
            return
        self.grid -= 1
        self.updated = True

        newcs = self.cellsize
        for elemento in self.elementos:
            elemento.resize(newcs)

    def shorterWindow(self):
        w, h = self.window.get_size()
        if min(w, h) < 100:
            return
        self.resize((w, h / Creator.SIZE_INCREMENT))

    def tallerWindow(self):
        w, h = self.window.get_size()
        if min(w, h) < 100:
            return
        self.resize((w, h * Creator.SIZE_INCREMENT))

    def thinerWindow(self):
        w, h = self.window.get_size()
        if min(w, h) < 100:
            return
        self.resize((w / Creator.SIZE_INCREMENT, h))

    def thickerWindow(self):
        w, h = self.window.get_size()
        if min(w, h) < 100:
            return
        self.resize((w * Creator.SIZE_INCREMENT, h))

    def changeElementType(self):
        if self.selected is None or self.movingSelected:
            return

        idx = self.elementos.index(self.selected)
        e = self.elementos[idx]

        newe = {
            Objeto.__name__: Aliado,
            Aliado.__name__: Enemigo,
            Enemigo.__name__: Objeto}[e.__class__.__name__](
                e.data(), e.cellsize)

        self.elementos[idx] = self.selected = newe
        self.updated = True

    def selectElemento(self):

        prev = self.selected
        if prev is not None:
            self.dropElemento()

        x, y = self.input.mousepos
        for item in self.elementos:
            if item.inside(x, y):
                self.selected = item
                break

        self.updated = self.selected is not prev

        return

    def dropElemento(self):

        if self.selected is None:
            self.updated = False
            return

        self.elementos.pop(self.elementos.index(self.selected))
        self.elementos.insert(0, self.selected)

        if not self.movingSelected:
            return

        x, y = self.input.mousepos
        cs = self.cellsize
        newx = (x // cs) * cs
        newy = (y // cs) * cs

        if x != newx or y != newy:
            self.history.append((
                self.selected,
                (self.selected.posx, self.selected.posy)))
            self.reversehistory.clear()

        self.selected.posx = newx
        self.selected.posy = newy

        # self.selected = None
        self.updated = True

    def removeSelected(self):
        if not self.selected or self.movingSelected:
            return

        self.elementos.remove(self.selected)

        del self.selected
        self.selected = None
        self.updated = True

        return

    def addElement(self):
        if self.selected and self.movingSelected:
            return

        imgfile = askopenfilename(
            title='Seleccionar una imagen para el elemento',
            initialdir=RESOURCEPATH)
        if not imgfile:
            return
        self.selected = Objeto(imgfile, self.cellsize)
        self.elementos.append(self.selected)
        self.updated = True

        return

    # Loopmethods

    def update(self):
        # if any(self.input.keypressed):
        #     print(self.input)

        self.updated = True

        if self.movingSelected:
            if not self.input.leftclicking:
                self.dropElemento()
                self.movingSelected = False
            return
        if self.input.rightclicking:
            self.selected = None
            return
        if self.input.leftclicking and not self.input.old_click[0]:
            self.movingSelected = False
            self.selectElemento()
            self.movingSelected = True
            return

        'S / S+Shift : Bigger/Smaller size category of element'
        if self.selected is not None:
            if self.input.keyunicode == 's':
                if self.selected.sizecategory >= self.grid:  # TEMP
                    return
                self.selected.biggerCategory()
                return
            elif self.input.keyunicode == 'S':
                self.selected.smallerCategory()
                return

        'Esc - close or unselect element'
        if self.input.keyname == 'escape':
            if self.visibleHelp:
                self.visibleHelp = False
            elif self.selected is not None:
                self.selected = None
            else:
                self.updated = False
            return

        if self.visibleHelp:
            if any(self.input.click):
                self.visibleHelp = False
            elif self.input.keyunicode == 'h':
                self.visibleHelp = False
            else:
                self.updated = False

            return

        'H : Show/hide this help message'
        if self.input.keyunicode.lower() == 'h':
            self.visibleHelp = True
            return

        'G : Show/hide grid'
        if self.input.keyunicode.lower() == 'g':
            self.visibleGrid = not self.visibleGrid
            return

        self.updated = False
        'B : Choose new background'
        if self.input.keyunicode.lower() == 'b':
            self.chooseBackground()
            return

        '+ / - : Bigger/Smaller grid'
        if self.input.keyunicode == '+':
            self.smallerGrid()
            return
        if self.input.keyunicode == '-':
            self.biggerGrid()
            return

        'W / W+Shift : More/Less max width',
        if self.input.keyunicode == 'w':
            self.thickerWindow()
            return
        if self.input.keyunicode == 'W':
            self.thinerWindow()
            return

        'T / T+Shift : More/Less max tallness',
        if self.input.keyunicode == 't':
            self.tallerWindow()
            return
        if self.input.keyunicode == 'T':
            self.shorterWindow()
            return

        'R : Change type of element',
        if self.input.keyunicode.lower() == 'r':
            self.changeElementType()
            return

        'A : Add object',
        if self.input.keyunicode.lower() == 'a':
            self.addElement()
            return

        'Backspace'
        if self.input.keyname == 'backspace':
            self.removeSelected()
            return

        return

    def show(self):

        if not self.updated:
            return
        print(self.tickN, '                 ', end='\r')
        self.window.blit(self.background, (0, 0))

        if self.visibleGrid:
            self.showgrid()

        for elemento in self.elementos[::-1]:
            if elemento is self.selected:
                elemento.show(self.window, backprint=(80, 80, 250))
            else:
                elemento.show(self.window)

        if self.movingSelected and self.selected is not None:  # Moviendo
            prev = self.selected.posx, self.selected.posy
            x, y = self.input.mousepos
            x -= self.cellsize / 2
            y -= self.cellsize / 2
            self.selected.posx, self.selected.posy = x, y
            self.selected.show(self.window, True, (80, 80, 250))
            self.selected.posx, self.selected.posy = prev

        if self.visibleHelp:
            self.showhelp()

        pg.display.update()
        self.updated = False

    def __str__(self):
        return f'{self.__class__.__name__}{vars(self)}'

    def __repr__(self) -> str:
        return str(self)


'''
if __name__ == '__main__':
    folderpath = './encounters/'
    # file = Creator().create(folderpath)
    file = Creator().createFromJSON('./encounters/forest.json')
    print(file)
'''

if __name__ == '__main__':
    from guitools.menu import Menu
    from os.path import exists, isfile

    # Ultima carpeta usada
    lastfolder_reg = '.lastdir'
    folder = None
    if exists(lastfolder_reg) and isfile(lastfolder_reg):
        with open(lastfolder_reg, 'r') as f:
            folder = f.read()
        if not folder or not exists(folder):
            folder = None

    # Seleccion de fichero existente
    menu = Menu(
        addFileButton=False,
        folderPath=folder)

    file, new = menu.loop()
    if file is None and not new:
        exit()

    # Ultima carpeta usada
    with open(lastfolder_reg, 'w') as f:
        f.write(dirname(file))

    # Edicion o creacion del encuentro
    print(file, new, menu.currentFolder)
    if new:
        file = Creator().create(menu.currentFolder)
    else:
        file = Creator().createFromJSON(file)

    print(file)
