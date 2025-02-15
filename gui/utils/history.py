
from typing import Callable, Generic, TypeVar

T = TypeVar('T')


class Memento(Generic[T]):
    def __init__(
            self,
            action: Callable,
            args: tuple[T, ...],
            reverse_action: Callable,
            reverse_args: tuple[T, ...]
            ) -> None:
        self.action = action
        self.args = args
        self.reverse_action = reverse_action
        self.reverse_args = reverse_args


class History:

    def __init__(self) -> None:
        self._past: list[Memento] = []
        self._future: list[Memento] = []

    def get_n_undoable(self) -> int:
        return len(self._past)

    def get_n_redoable(self) -> int:
        return len(self._future)

    def do(
            self, action: Callable, aargs: tuple,
            rev_action: Callable, rargs: tuple) -> Memento:
        memento = Memento(action, aargs, rev_action, rargs)
        memento.action(*memento.args)
        self._past.append(memento)
        self._future.clear()
        return memento

    def redo(self) -> Memento:
        memento = self._future.pop()
        self._past.append(memento)
        memento.action(*memento.args)
        return memento

    def undo(self) -> Memento:
        memento = self._past.pop()
        self._future.append(memento)
        memento.reverse_action(*memento.reverse_args)
        return memento
