
from pygame import Surface
import pygame as pg

from gui.utils.image import ImageUtils
from gui.model.creature import CreatureModel
from gui.values import CreatureStatus, CreatureTeam, ImageShape
from gui.view.entity import EntityView


class CreatureView(EntityView):
    _model: CreatureModel  # type:ignore

    def draw_surface(self) -> Surface:
        surface = super().draw_surface()

        x, y = surface.get_size()
        match self._model.status:
            case CreatureStatus.ALIVE:
                ...
            case CreatureStatus.SLEEP:
                sf = pg.font.SysFont('roboto', y, True)
                s = sf.render('S', True, (0, 0, 0), (250, 250, 250))
                s.set_alpha(100)
                s = ImageUtils.fit(s, (x//1.5, y//1.5))
                w, h = s.get_size()
                surface.blit(s, ((x-w) // 2, (y-h) // 2))
            case CreatureStatus.DEAD:
                thick = round((x + y) / 2 * 0.08)
                offset = (x + y) / 2 * 0.1
                pg.draw.line(
                    surface, (0, 0, 0), (offset, offset),
                    (x - offset, y - offset), thick)
                pg.draw.line(
                    surface, (0, 0, 0), (offset, y - offset),
                    (x - offset, offset), thick)
            case _:
                raise ValueError(
                    f'Status "{self._model.status.value}" not supported')

        aura = None
        match self._model.team:
            case CreatureTeam.NONE:
                ...
            case CreatureTeam.ALLY:
                aura = (80, 250, 80)
            case CreatureTeam.ENEMY:
                aura = (250, 80, 80)
            case _:
                raise ValueError(
                    f'Team "{self._model.team.value}" not supported')

        if aura is not None:
            thick = round((x + y) / 2 * 0.06)
            if self._model.shape == ImageShape.CIRCULAR:
                rad = min(x, y) // 2
                pg.draw.circle(
                    surface, aura, (
                        surface.get_width() // 2,
                        surface.get_height() // 2),
                    rad, thick)
            else:
                rad = -1
                pg.draw.rect(surface, aura, (0, 0, x, y), thick, rad)

        return surface
