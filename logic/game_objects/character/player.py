from logic.game_objects.character.action import ActionType
from logic.game_objects.character.character import Character
from logic.game_objects.map.element import MapElementInGame
from logic.game_objects.position import Position
from logic.game_objects.character.moving import PlayerMovingMixin


class Player(Character,
             PlayerMovingMixin):
    # точка персонажа на карте, то, где его будут обрабатывать (на данный момент низ топ)

    def __init__(self, spawn_point: Position = Position(0, 0)):
        super().__init__(spawn_point=spawn_point)
        PlayerMovingMixin.__init__(self)

    def moving(self, surface: MapElementInGame):
        super(Player, self).moving(surface)
        self.update()
        self.stop(swap_sprite=False,
                  surface=surface)

