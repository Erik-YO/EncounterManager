

import pygame as pg
from pygame import Surface
from pathlib import Path
from typing import Any, Literal
from math import ceil

from gui.controller.background import BackgroundController
from gui.controller.creature import CreatureController
from gui.values import CreatureStatus, CreatureTeam, ImageShape
from gui.controller.entity import EntityController
from gui.controller.item import ItemController
from gui.utils.history import History
from gui.menu.menu import Menu
from gui.utils import report


class Encounter(Menu):

    HIGHLIGHT_COLOR = (240, 240, 60, 128)

    def __init__(
            self, background: BackgroundController,
            entities: list[EntityController],
            min_units: int) -> None:
        self.background = background
        self.entities = entities

        self.min_units = min_units

        self.history = History()

        self.grid_visible: bool = False
        self.selected: EntityController | None = None
        self.updated = True

        cell_size = min(self.get_size()) / self.min_units
        for m in self.entities:
            m.change_cell_size(cell_size)

    def to_dict(self) -> dict[str, Any]:
        c = [
            c.model.to_dict() for c in self.entities
            if isinstance(c, CreatureController)]

        i = [
            i.model.to_dict() for i in self.entities
            if isinstance(i, ItemController)]

        return {
            'creatures': c,
            'items': i,
            'background': self.background.model.to_dict(),
            'min_units': self.min_units,
        }

    @staticmethod
    def new(background_image: Path):
        return Encounter(
            BackgroundController.from_dict(
                {'img': str(background_image)}),
            [], 8)

    @staticmethod
    def from_dict(encounter_data: dict[str, int | float | str]) -> 'Encounter':

        cdata = encounter_data.get('creatures', [])
        assert isinstance(cdata, list)
        assert all(isinstance(c, dict) for c in cdata)
        creatures = [CreatureController.from_dict(c) for c in cdata]

        idata = encounter_data.get('items', [])
        assert isinstance(idata, list)
        assert all(isinstance(i, dict) for i in idata)
        items = [ItemController.from_dict(c) for c in idata]

        entities: list[EntityController] = []
        entities.extend(creatures)
        entities.extend(items)

        bg_data = encounter_data.get('background')
        assert isinstance(bg_data, dict), (
            'background field should be a dict, not '
            f'{type(bg_data).__name__}: {bg_data}')
        bg = BackgroundController.from_dict(bg_data)

        scale = encounter_data.get("scale", 1.0)
        assert isinstance(scale, float)
        mu = encounter_data.get("min_units")
        assert isinstance(mu, int)

        return Encounter(bg, entities, mu)

    # Loopable

    def render(self, window: Surface):
        # Background
        self.background.render(window)

        cell_size = min(self.get_size()) / self.min_units

        if self.grid_visible:
            self.render_grid(window, cell_size)

        # TODO: Area effects

        # Highlight selected
        if self.selected:
            self.render_highlight(window, self.selected, cell_size)

        # Entities
        for e in self.entities[::-1]:
            e.render(window, cell_size)

        self.updated = False

    def render_highlight(
            self, window: Surface, entity: EntityController, cell_size: float):
        x, y = entity.model.x * cell_size, entity.model.y * cell_size
        w, h = entity.view.get_surface().get_size()

        if entity.model.shape is ImageShape.CIRCULAR:
            thick = 4
            pg.draw.circle(
                window, Encounter.HIGHLIGHT_COLOR, (x + w // 2, y + h // 2),
                max(w, h) // 2 + thick, thick + 1)
        else:
            offset = (w / 2, h / 2) if entity.model.size < 1 else (0, 0)
            pg.draw.rect(
                window, Encounter.HIGHLIGHT_COLOR,
                (x - 3 + offset[0], y - 3 + offset[1], w + 6, h + 6))

    def render_grid(self, window: Surface, cell_size: float):

        w, h = self.get_size()
        x = y = cell_size
        white, black = (200, 200, 200), (0, 0, 0)
        for _ in range(ceil(w / cell_size)):
            pg.draw.line(window, white, (x, 0), (x, h))
            pg.draw.line(window, black, (x + 1, 0), (x + 1, h))
            x += cell_size
        for _ in range(ceil(h / cell_size)):
            pg.draw.line(window, white, (0, y), (w, y))
            pg.draw.line(window, black, (0, y + 1), (w, y + 1))
            y += cell_size

    # Getters

    def get_entity(self, px_x: int, px_y: int) -> EntityController | None:
        cell_size = min(self.get_size()) / self.min_units

        for entity in self.entities:
            if entity.is_hovering(px_x, px_y, cell_size):
                return entity
        return None

    def get_size(self) -> tuple[int, int]:
        return self.background.view.get_surface().get_size()

    # Checks & internal

    def find_entity(self, entity: EntityController) -> int:
        try:
            return self.entities.index(entity)
        except ValueError:
            return -1

    def _add_entity(self, entity: EntityController):
        self.entities.insert(0, entity)
        self.selected = entity
        self.updated = True

    def _rev_add_entity(
            self, entity: EntityController,
            prev_selected: EntityController | None):
        idx = self.find_entity(entity)
        self.entities.pop(idx)
        self.selected = prev_selected
        self.updated = True

    def _remove_entity(self, entity: EntityController):
        idx = self.find_entity(entity)
        if idx >= 0:
            self.entities.pop(idx)
            if self.selected is entity:
                self.selected = None
            self.updated = True

    def _rev_remove_entity(
            self, entity: EntityController, idx: int, was_selected: bool):
        self.entities.insert(idx, entity)
        if was_selected:
            self.selected = entity
        self.updated = True

    def _set_grid(self, min_units: int):
        if min_units < 1:
            return

        changed = self.min_units != min_units
        self.min_units = min_units
        csize = min(self.get_size()) / self.min_units
        for e in self.entities:
            e.change_cell_size(csize)

        self.updated |= changed

    def _set_background_image(self, image: Path):
        self.background.change_image(image)
        self.updated = True

    def _set_selected(self, selected_idx: int | None):
        if selected_idx is None:
            self.updated |= self.selected is not None
            self.selected = None
            return

        new = self.entities.pop(selected_idx)
        self.entities.insert(0, new)
        self.selected = new
        self.updated |= new != self.selected

    def _unset_selected(self, prev_selected: bool, old_idx: int | None):
        if old_idx is not None:
            self.entities.insert(old_idx, self.entities.pop(0))
        self.selected = self.entities[0] if prev_selected else None
        self.updated = True

    def _set_entity_position(self, entity: EntityController, x: int, y: int):
        self.updated |= (entity.model.x, entity.model.y) != (x, y)
        entity.move(x, y)

    def _set_entity_pos_bulk(
            self, entities: list[EntityController],
            new_pos: list[tuple[int, int]]):
        for e, (x, y) in zip(entities, new_pos):
            e.move(x, y)
        self.updated |= any(
            (e.model.x, e.model.y) != p
            for e, p in zip(entities, new_pos))

    def _set_creature_team(
            self, creature: CreatureController, team: CreatureTeam):
        self.updated |= creature.get_team() != team
        creature.set_team(team)

    def _set_creature_status(
            self, creature: CreatureController, status: CreatureStatus):
        self.updated |= creature.get_status() != status
        creature.set_status(status)

    def _grow_entity(self, entity: EntityController):
        self.updated |= True
        entity.grow()

    def _shrink_entity(self, entity: EntityController):
        self.updated |= True
        entity.shrink()

    def _replace_entity(self, old: EntityController, new: EntityController):
        idx = self.find_entity(old)
        if idx < 0:
            report.error('_replace_entity not found')
            return
        self.entities[idx] = new
        if self.selected is old:
            self.selected = new
        self.updated = True

    def _scale(self, new_scale: float):
        self.background.set_scale(new_scale)
        csize = min(self.get_size()) / self.min_units
        for e in self.entities:
            e.change_cell_size(csize)
        self.updated = True

    # Commands

    # Background

    def change_background(self, new_image: Path):
        report.info('change_background')
        self.history.do(
            self._set_background_image, (new_image, ),
            self._set_background_image,
            (self.background.model.get_image_path(), ))

    def reduce_grid(self):
        report.info('reduce_grid')
        self.history.do(
            self._set_grid, (self.min_units + 1, ),
            self._set_grid, (self.min_units, ))

    def enlarge_grid(self):
        if self.min_units <= 1:
            report.info('enlarge_grid not completed, limit reached')
            return
        report.info('enlarge_grid')
        self.history.do(
            self._set_grid, (self.min_units - 1, ),
            self._set_grid, (self.min_units, ))

    def enlarge_window(self, factor: float):
        if factor <= 1:
            report.warning(
                f'enlarge_window not completed, factor {factor} <= 1')
            return
        report.info('enlarge_window')
        old = self.background.model.scale
        self.history.do(
            self._scale, (factor * old, ),
            self._scale, (old, ))

    def shrink_window(self, factor: float):
        if factor >= 1:
            report.warning(
                f'shrink_window not completed, factor {factor} >= 1')
            return
        report.info('shrink_window')
        old = self.background.model.scale
        self.history.do(
            self._scale, (factor * old, ),
            self._scale, (old, ))

    # Individual entities

    def select_entity(self, entity: EntityController):
        idx = self.find_entity(entity)
        if idx < 0:
            report.warning('select_entity not completed, entity not found')
            return

        if self.entities[idx] is self.selected:
            report.info('select_entity not completed, already selected')
            return
        report.info('select_entity')

        self.history.do(
            self._set_selected, (idx, ),
            self._unset_selected, (self.selected is not None, idx))

    def deselect_entity(self):
        if self.selected is None:
            report.info('deselect_entity not completed, none selected')
            return
        report.info('deselect_entity')
        self.history.do(
            self._set_selected, (None, ),
            self._unset_selected, (True, None))

    def move_entity(
            self, entity: EntityController,
            px_x: int | float, px_y: int | float):
        if self.find_entity(entity) < 0:
            report.info('move_entity not completed, entity not found')
            return
        report.info('move_entity')

        cell_size = min(self.get_size()) / self.min_units

        # Adjustment for different size categories
        v = (entity.model.size - 1) / 2 if entity.model.size > 1 else 0
        report.info(
            f'{px_x, px_y} -> {px_x - v * cell_size, px_y - v * cell_size} '
            f'({cell_size})')
        px_x -= v * cell_size
        px_y -= v * cell_size

        x, y = int(px_x / cell_size), int(px_y / cell_size)

        self.history.do(
            self._set_entity_position, (entity, x, y),
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y))

    def move_entity_right(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('move_entity_right not completed, entity not found')
            return
        report.info('move_entity_right')
        self.history.do(
            self._set_entity_position,
            (entity, entity.model.x + 1, entity.model.y),
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y))

    def move_entity_left(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('move_entity_left not completed, entity not found')
            return
        report.info('move_entity_left')
        self.history.do(
            self._set_entity_position,
            (entity, entity.model.x - 1, entity.model.y),
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y))

    def move_entity_up(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('move_entity_up not completed, entity not found')
            return
        report.info('move_entity_up')
        self.history.do(
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y - 1),
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y))

    def move_entity_down(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('move_entity_down not completed, entity not found')
            return
        report.info('move_entity_down')
        self.history.do(
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y + 1),
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y))

    def bring_home(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('bring_home not completed, entity not found')
            return
        report.info('bring_home')
        w, h = self.get_size()
        csize = min(w, h) / self.min_units
        maxx, maxy = int(w / csize), int(h / csize)

        x = max(0, min(maxx - ceil(entity.model.size), entity.model.x))
        y = max(0, min(entity.model.y, maxy - ceil(entity.model.size)))
        report.info(f'{entity.model.x, entity.model.y} -> {x, y}')
        self.history.do(
            self._set_entity_position,
            (entity, x, y),
            self._set_entity_position,
            (entity, entity.model.x, entity.model.y))

    def change_entity_type(self, entity: EntityController):
        idx = self.find_entity(entity)
        if idx < 0:
            report.info('change_creature_type not completed, not found')
            return
        report.info('change_entity_type')

        old = type(entity)
        match old.__name__:
            case 'CreatureController':
                new = ItemController
            case 'ItemController':
                new = CreatureController
            case _other:
                report.error(
                    'change_entity_type current type '
                    f'"{_other}" not supported')
                return

        newe = new.from_dict(
            entity.model.to_dict(), min(self.get_size()) / self.min_units)

        self.history.do(
            self._replace_entity, (entity, newe),
            self._replace_entity, (newe, entity))

    def change_creature_team(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('change_creature_team not completed, not found')
            return
        if not isinstance(entity, CreatureController):
            report.info('change_creature_team not completed, not a creature')
            return
        report.info('change_creature_team')
        old = entity.get_team()
        new_team = old.next()
        self.history.do(
            self._set_creature_team, (entity, new_team),
            self._set_creature_team, (entity, old))

    def change_creature_status(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('change_creature_status not completed, not found')
            return
        if not isinstance(entity, CreatureController):
            report.info('change_creature_status not completed, not a creature')
            return
        report.info('change_creature_status')
        old = entity.get_status()
        new_status = old.next()
        self.history.do(
            self._set_creature_status, (entity, new_status),
            self._set_creature_status, (entity, old))

    def grow_entity(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('grow_entity not completed, not found')
            return
        report.info('grow_entity')
        self.history.do(
            self._grow_entity, (entity, ),
            self._shrink_entity, (entity, ))

    def shrink_entity(self, entity: EntityController):
        if self.find_entity(entity) < 0:
            report.info('shrink_entity not completed, not found')
            return
        report.info('shrink_entity')
        self.history.do(
            self._shrink_entity, (entity, ),
            self._grow_entity, (entity, ))

    # Globals

    def bring_all_home(self):
        report.info('bring_all_home')
        w, h = self.get_size()
        csize = min(w, h) / self.min_units
        maxx, maxy = int(w / csize), int(h / csize)

        new_pos = [
            (
                max(0, min(maxx - ceil(e.model.size), e.model.x)),
                max(0, min(e.model.y, maxy - ceil(e.model.size))))
            for e in self.entities]
        old_pos = [(e.model.x, e.model.y) for e in self.entities]
        self.history.do(
            self._set_entity_pos_bulk, (self.entities, new_pos),
            self._set_entity_pos_bulk, (self.entities, old_pos))

    def create_creature(self, image: Path):
        report.info('create_creature')
        c = CreatureController.from_dict(
            {'img': str(image)}, min(self.get_size()) / self.min_units)
        self.history.do(
            self._add_entity, (c, ),
            self._rev_add_entity, (c, self.selected))

    def create_item(self, image: Path):
        report.info('create_item')
        i = ItemController.from_dict(
            {'img': str(image)}, min(self.get_size()) / self.min_units)
        self.history.do(
            self._add_entity, (i, ),
            self._rev_add_entity, (i, self.selected))

    def destroy_entity(self, entity: EntityController):
        report.info('destroy_entity')
        idx = self.find_entity(entity)
        if idx < 0:
            report.info('destroy_entity not completed, not found')
            return
        self.history.do(
            self._remove_entity, (entity,),
            self._rev_remove_entity,
            (entity, idx, entity is self.selected))

    # History

    def undo(self):
        if self.history.get_n_undoable() < 1:
            report.info('undo not completed, no actions left')
            return
        report.info('undo')
        self.history.undo()

    def redo(self):
        if self.history.get_n_redoable() < 1:
            report.info('redo not completed, no actions left')
            return
        report.info('redo')
        self.history.redo()
