
from gui.model.entity import EntityModel
from gui.values import CreatureStatus, CreatureTeam, ImageShape


class CreatureModel(EntityModel):
    status = CreatureStatus.ALIVE
    team = CreatureTeam.NONE
    shape = ImageShape.CIRCULAR

    def __init__(self, status: CreatureStatus, team: CreatureTeam) -> None:
        self.status = status
        self.team = team

    def to_dict(self) -> dict[str, int | float | str]:
        return super().to_dict() | ({
            'status': self.status.value
        } if self.status != type(self).status else {}) | ({
            'team': self.team.value
        } if self.team != type(self).team else {})

    @classmethod
    def from_dict(
            cls, element_data: dict[str, str | int | float]
            ):

        status = element_data.get('status', cls.status.value)
        assert CreatureStatus.has_value(status), (
            'The creature status must be one of the supported '
            f'options {tuple(s.value for s in CreatureStatus)},'
            f' not {repr(status)}')
        status = CreatureStatus(status)

        team = element_data.get('team', cls.team.value)
        assert CreatureTeam.has_value(team), (
            'The creature team must be one of the supported '
            f'options {tuple(s.value for s in CreatureTeam)},'
            f' not {repr(team)}')
        team = CreatureTeam(team)

        cm = super().from_dict(element_data)
        CreatureModel.__init__(cm, status, team)
        return cm

    def set_status(self, status: CreatureStatus):
        self.status = status

    def set_team(self, team: CreatureTeam):
        self.team = team
