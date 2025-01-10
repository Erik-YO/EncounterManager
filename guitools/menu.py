
from os.path import join, abspath, dirname, isdir, isfile, exists
from os import listdir
from typing import Optional, List
from .userinput import Input
import pygame as pg
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Menu:

    LINE_HEIGHT = 30
    MAX_LINES = 8  # Min = 3
    BACKGROUND_COLOR = (53, 144, 243)
    HOVER_COLOR = (98, 191, 237)

    def __init__(
            self,
            addFileButton: bool = False,
            folderPath: Optional[str] = None) -> None:

        if folderPath is None:
            folderPath = join(dirname(__file__), '..')
        folderPath = abspath(folderPath)

        if not isdir(folderPath):
            raise ValueError(f'{folderPath} no es un directorio valido')

        # Graphic
        self.window: pg.Surface = None
        self.font: pg.font.Font = None

        # Contents
        self.currentFolder: str = folderPath
        self.currentFiles: List[str] = []
        self.addFileButton: bool = addFileButton

        # State
        self.hoverSlot: int = 0
        self.firstIdx: int = 0

        # Input
        self.input = Input()
        self.updated: bool = True

        # Out
        self.fileSelected: str = None
        self.createNewFile: bool = False

    def setCurrentFiles(self):
        self.currentFiles = [
            f'{f}/' if isdir(f) else f
            for f in listdir(self.currentFolder)
            if exists(join(self.currentFolder, f))
        ]
        print(' > ', self.currentFiles, self.currentFolder)

        if self.currentFiles:
            mw = max(self.font.size(f)[0] for f in self.currentFiles)
        else:
            mw = 96

        self.window = pg.display.set_mode(
            (mw + 4, Menu.LINE_HEIGHT * Menu.MAX_LINES))

        caption = (
            f'Choose encounter {self.currentFolder[len("c:/users/"):][-20:]}')
        pg.display.set_caption(caption)
        print('New folder:', caption)
        self.firstIdx = 0

    def init(self):
        pg.init()
        pg.font.init()

        self.font = pg.font.SysFont('arial', Menu.LINE_HEIGHT - 2)

        self.setCurrentFiles()

    def close(self):
        pg.font.quit()
        pg.quit()

    def loop(self):
        # TEMP
        """
        """
        if self.addFileButton:
            file = asksaveasfilename(
                initialdir=self.currentFolder,
                title='Eleccion de fichero de configuracion')
        else:
            file = askopenfilename(
                initialdir=self.currentFolder,
                title='Eleccion de fichero de configuracion')

        self.fileSelected, self.createNewFile = file, not file
        return self.fileSelected, self.createNewFile

        self.init()

        clock = pg.time.Clock()
        while (
                not self.input.quit and
                not self.fileSelected and
                not self.createNewFile):
            self.show()
            clock.tick(20)
            self.input.fromEvents(pg.event.get())
            self.update()

        self.close()

        return self.fileSelected, self.createNewFile

    def update(self):

        if self.input.mousemoved:
            self.hoverSlot = self.input.mousey // Menu.LINE_HEIGHT
            self.updated = True

        if self.input.keyname == 'up':
            if self.hoverSlot > 0:
                self.hoverSlot -= 1
                self.updated = True

        elif self.input.keyname == 'down':
            if self.hoverSlot < Menu.MAX_LINES - 1:
                self.hoverSlot += 1
                self.updated = True

        elif self.input.keyname == 'return' or self.input.leftclick:
            self.updated = True
            if self.hoverSlot == 0:
                newfolder = dirname(self.currentFolder)
                if len(newfolder) > len('C:/users/'):
                    self.currentFolder = newfolder
                    self.setCurrentFiles()

            elif self.hoverSlot >= Menu.MAX_LINES - 1:
                self.createNewFile = True

            else:
                file = abspath(join(
                    self.currentFolder,
                    self.currentFiles[self.firstIdx - 1 + self.hoverSlot]))

                if isdir(file):
                    self.currentFolder = file
                    self.setCurrentFiles()
                elif isfile(file):
                    self.fileSelected = file

        return

    def show(self):

        if not self.updated:
            return

        self.window.fill(Menu.BACKGROUND_COLOR)

        lines = self.currentFiles[
            self.firstIdx:self.firstIdx + Menu.MAX_LINES - 1]
        if self.addFileButton and lines:
            lines.pop()

        if not self.hoverSlot:
            self.window.fill(
                Menu.HOVER_COLOR, (
                    0, 0, self.window.get_width(), Menu.LINE_HEIGHT))

        text = self.font.render('../', True, (0, 0, 0))
        self.window.blit(text, (2, Menu.LINE_HEIGHT - text.get_height()))
        for idx, line in enumerate(lines, 1):
            if self.hoverSlot == idx:
                self.window.fill(
                    Menu.HOVER_COLOR, (
                        0, Menu.LINE_HEIGHT * idx,
                        self.window.get_width(), Menu.LINE_HEIGHT))
            pg.draw.line(
                self.window, (0, 0, 0),
                (0, idx * Menu.LINE_HEIGHT),
                (self.window.get_width(), idx * Menu.LINE_HEIGHT))

            text = self.font.render(line, True, (0, 0, 0))

            self.window.blit(
                text,
                (2, idx * Menu.LINE_HEIGHT))

        if self.addFileButton:
            if self.hoverSlot >= Menu.MAX_LINES - 1:
                self.window.fill(
                    Menu.HOVER_COLOR, (
                        0, Menu.LINE_HEIGHT * (Menu.MAX_LINES - 1),
                        self.window.get_width(), Menu.LINE_HEIGHT))
            pg.draw.line(
                self.window, (0, 0, 0),
                (0, (Menu.MAX_LINES - 1) * Menu.LINE_HEIGHT), (
                    self.window.get_width(),
                    (Menu.MAX_LINES - 1) * Menu.LINE_HEIGHT))
            text = self.font.render('+', True, (0, 0, 0))
            self.window.blit(
                text, (
                    (self.window.get_width() - text.get_width()) / 2,
                    Menu.MAX_LINES * Menu.LINE_HEIGHT - (
                        Menu.LINE_HEIGHT + text.get_height()) / 2))

        pg.display.update()
        self.updated = False
