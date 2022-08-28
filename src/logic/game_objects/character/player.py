from src.logic.game_objects.character.mechanics.character import Character
from src.logic.game_objects.map.element import MapElementInGame
from src.logic.game_objects.position import Position
from src.logic.game_objects.character.mechanics.moving import PlayerMovingMixin


class Player(Character,
             PlayerMovingMixin):
    # точка персонажа на карте, то, где его будут обрабатывать (на данный момент низ топ)

    def __init__(self, spawn_point: Position = Position(0, 0)):
        super().__init__(spawn_point=spawn_point)
        PlayerMovingMixin.__init__(self)

    def moving(self,
               pressed_button: int | None = None):
        surface = self.get_map_element_under_character()
        super(Player, self).moving(surface, pressed_button=pressed_button)
        self.update()
        print(self.rect)
        # print(self.player_level)
        self.stop(swap_sprite=False,
                  surface=surface)

