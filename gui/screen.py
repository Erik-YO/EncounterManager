
from pathlib import Path
from tkinter.filedialog import askopenfilename

from pygame import Surface
import pygame as pg

from gui.controller.entity import EntityController
from gui.menu.encounter import Encounter
from gui.user_input import UserInput
from gui.files import IMAGE_FILETYPES, image_dir


class Screen:
    GHOST_TRANSPARENCY = (255, 255, 255, 128)
    WINDOW_ENLARGE_FACTOR = 1.15
    WINDOW_SHRINK_FACTOR = 0.85

    def __init__(self, encounter: Encounter) -> None:
        self._precalc: Surface = Surface(
            encounter.get_size(), pg.BLEND_RGBA_MULT)
        self._last_ghost: tuple[EntityController, Surface] | None = None

        self.input = UserInput()
        self.encounter = encounter
        self.window = pg.display.set_mode(self._precalc.get_size())
        pg.display.set_caption('EncounterManager')
        self.ghost_active: bool = False
        self.updated = True

    @staticmethod
    def from_image(image: Path):
        return Screen(Encounter.new(image))

    @staticmethod
    def from_dict(data: dict):
        return Screen(Encounter.from_dict(data))

    @property
    def moving_entity(self) -> EntityController | None:
        if self.input.leftclicking:
            return self.encounter.selected
        return None

    def loop(self):

        clock = pg.time.Clock()
        while not self.input.quit:

            # Show
            self.show()
            clock.tick(20)

            # Input
            self.input.fromEvents(pg.event.get())

            # Update
            self.update()

    def show(self):
        # TODO: Menus

        # Encounter
        if self.updated:
            self.encounter.render(self._precalc)

            # Selected entity ghost
            self.render_selected_ghost()

        self.window.blit(self._precalc, (0, 0))
        pg.display.update()

    def render_selected_ghost(self):
        entity = self.moving_entity
        if entity is None:
            return

        if self._last_ghost is None or self._last_ghost[0] is not entity:

            surf = entity.view.get_surface().copy()
            surf.fill(Screen.GHOST_TRANSPARENCY, None, pg.BLEND_RGBA_MULT)
            self._last_ghost = (entity, surf)

        g = self._last_ghost[1]
        self._precalc.blit(g, (
            self.input.mousex - g.get_width() // 2,
            self.input.mousey - g.get_height() // 2))

    def update(self):
        self.updated = False

        if self.input.leftclick:
            e = self.encounter.get_entity(*self.input.mousepos)
            if e is not None:
                self.encounter.select_entity(e)
                self.ghost_active = True
                self._last_ghost = None
            self.updated = True

        if self.input.leftunclick:
            if self.encounter.selected:
                self.encounter.move_entity(
                    self.encounter.selected, *self.input.mousepos)
                self.updated = True
            self.ghost_active = False

        if self.input.leftclicking:
            self.updated = True

        # TESTING

        '''if self.ghost_active:
            self.updated |= self.input.mousepos != self.input.old_mousepos

        if self.input.leftclick:
            entity = self.encounter.get_entity(*self.input.mousepos)
            if self.encounter.selected is not None:
                self.encounter.move_entity(
                    self.encounter.selected, *self.input.mousepos)
                if entity is not self.encounter.selected:
                    self.encounter.deselect_entity()

            if entity is not None and entity is not self.encounter.selected:
                self.encounter.select_entity(entity)

            if entity is None and self.encounter.selected is None:
                self.ghost_active = False

        elif not self.input.leftclicking:
            self.ghost_active = False'''
        if not any(self.input.keypressed):
            return

        key_reg = True
        match self.input.keyunicode.upper():
            case 'B':
                image_path = askopenfilename(
                    initialdir=image_dir(),
                    title='Choose a new background image',
                    filetypes=(('Background image', IMAGE_FILETYPES), )
                )
                if image_path:
                    self.encounter.change_background(Path(image_path))

            case 'D':  # D
                self.encounter.grid_visible = not self.encounter.grid_visible
                self.encounter.updated = True

            case 'G':  # G
                self.encounter.reduce_grid()
            case '\x07':  # Ctrl + G
                self.encounter.enlarge_grid()

            case 'W':  # W
                self.encounter.enlarge_window(self.WINDOW_ENLARGE_FACTOR)
            case '\x17':  # Ctrl + W
                self.encounter.shrink_window(self.WINDOW_SHRINK_FACTOR)

            case 'C':  # C
                if self.encounter.selected is not None:
                    self.encounter.change_entity_type(
                        self.encounter.selected)
            case 'T':  # T
                if self.encounter.selected is not None:
                    self.encounter.change_creature_team(
                        self.encounter.selected)
            case 'S':  # S
                if self.encounter.selected is not None:
                    self.encounter.change_creature_status(
                        self.encounter.selected)

            case 'L':  # L
                if self.encounter.selected is not None:
                    self.encounter.grow_entity(
                        self.encounter.selected)
            case '\x0c':  # Ctrl + L
                if self.encounter.selected is not None:
                    self.encounter.shrink_entity(
                        self.encounter.selected)

            case 'H':  # H
                if self.encounter.selected is not None:
                    self.encounter.bring_home(self.encounter.selected)
            case '\x08':  # Ctrl + H
                self.encounter.bring_all_home()

            case 'A':  # A
                image_path = askopenfilename(
                    initialdir=image_dir(),
                    title='Choose an image for the new creature',
                    filetypes=(('Creature image', IMAGE_FILETYPES),),
                )
                if image_path:
                    self.encounter.create_creature(Path(image_path))
            case 'I':  # I
                image_path = askopenfilename(
                    initialdir=image_dir(),
                    title='Choose an image for the new item',
                    filetypes=(('Item image', IMAGE_FILETYPES),),
                )
                if image_path:
                    self.encounter.create_item(Path(image_path))

            case '\x1a':  # Ctrl + Z
                self.encounter.undo()
            case '\x19':  # Ctrl + Y
                self.encounter.redo()

            case '\x03':  # Ctrl + C
                # TODO
                ...
            case '\x16':  # Ctrl + V
                # TODO
                ...

            case _:
                key_reg = False

        if self.window.get_size() != self.encounter.get_size():
            self.window = pg.display.set_mode(
                self.encounter.get_size())
            pg.display.set_caption('EncounterManager')
            self._precalc = self.window.copy()
            self.updated = True

        if key_reg:
            self.updated = True
            return

        key_reg = True
        match self.input.keyname:
            case 'escape':  # Esc
                self.encounter.deselect_entity()

            case 'right':  # Right
                if self.encounter.selected is not None:
                    self.encounter.move_entity_right(self.encounter.selected)
            case 'left':  # Left
                if self.encounter.selected is not None:
                    self.encounter.move_entity_left(self.encounter.selected)
            case 'up':  # Up
                if self.encounter.selected is not None:
                    self.encounter.move_entity_up(self.encounter.selected)
            case 'down':  # Down
                if self.encounter.selected is not None:
                    self.encounter.move_entity_down(self.encounter.selected)

            case 'backspace' | 'delete':  # Supr, Del
                if self.encounter.selected is not None:
                    self.encounter.destroy_entity(self.encounter.selected)
            case _:
                key_reg = False

        self.updated |= key_reg

    @staticmethod
    def init():
        pg.init()
        pg.font.init()
        pg.display.init()
        pg.display.set_mode()
        pg.display.set_caption('EncounterManager')

    @staticmethod
    def close():
        pg.display.quit()
        pg.font.quit()
        pg.init()
