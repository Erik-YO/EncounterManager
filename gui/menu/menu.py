
from pygame import Surface

from gui.user_input import UserInput


class Menu:

    def render(self, window: Surface):
        ...

    def update(self, user_input: UserInput) -> bool:
        '''Return "propagate user_input also to next menu"'''
        ...
