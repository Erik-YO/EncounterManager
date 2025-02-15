
from enum import Enum
from typing import Any


class CiclableEnum(Enum):
    def next(self):
        members = list(self.__class__)
        index = members.index(self) + 1
        return members[index % len(members)]

    def prev(self):
        members = list(self.__class__)
        index = members.index(self) - 1
        return members[index % len(members)]

    @classmethod
    def has_value(cls, value: Any) -> bool:
        return value in (e.value for e in cls)


class ImageShape(CiclableEnum):
    ORIGINAL = 'original'
    CIRCULAR = 'circular'


class CreatureStatus(CiclableEnum):
    ALIVE = 'alive'
    SLEEP = 'sleep'
    DEAD = 'dead'


class CreatureTeam(CiclableEnum):
    NONE = 'none'
    ALLY = 'ally'
    ENEMY = 'enemy'
