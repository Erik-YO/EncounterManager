
from gui.controller.entity import EntityController
from gui.model.creature import CreatureModel
from gui.values import CreatureStatus, CreatureTeam
from gui.view.creature import CreatureView


class CreatureController(EntityController):
    view_class = CreatureView
    model_class = CreatureModel
    model: CreatureModel  # type:ignore
    view: CreatureView  # type:ignore

    @classmethod
    def from_dict(
            cls, element_data: dict[str, int | float | str],
            base_size: float | None = None):

        model = cls.model_class.from_dict(element_data)
        view = cls.view_class(
            model,
            cls.view_class.DEFAULT_BASE_SIZE
            if base_size is None else base_size)

        ec = super().__new__(cls)
        CreatureController.__init__(ec, model, view)
        return ec

    def change_status(self):
        new = self.model.status.next()
        assert isinstance(new, CreatureStatus)
        self.model.set_status(new)
        self.view.model_updated()

    def change_team(self):
        new = self.model.team.next()
        assert isinstance(new, CreatureTeam)
        self.model.set_team(new)
        self.view.model_updated()

    def set_team(self, new_team: CreatureTeam):
        old = self.model.team
        self.model.set_team(new_team)
        if old != new_team:
            self.view.model_updated()

    def set_status(self, new_status: CreatureStatus):
        old = self.model.status
        self.model.set_status(new_status)
        if old != new_status:
            self.view.model_updated()

    def get_team(self) -> CreatureTeam:
        return self.model.team

    def get_status(self) -> CreatureStatus:
        return self.model.status
