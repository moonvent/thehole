from logic.game_objects.action import ActionType
from logic.game_objects.character.character import Character
from logic.game_objects.position import Position
from logic.game_objects.character.moving import PlayerMovingMixin, MoveDirection


class Player(Character,
             PlayerMovingMixin):
    def __init__(self):
        super().__init__()
        PlayerMovingMixin.__init__(self)
        self.spawn_point = Position(0, 0)
        self.Direction = MoveDirection.Right

    def moving(self, action_type: ActionType):
        super(Player, self).moving(action_type)
        self.update()
        self.stop(swap_sprite=False,
                  action_type=action_type)

