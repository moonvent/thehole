from logic.game_objects.action import ActionType
from pygame.sprite import Sprite
from pygame.surface import Surface


class MapElement(Sprite):
    constant: bool = False      # будет ли накладываться картинка поверх персонажа

    def __init__(self,
                 x: int,
                 y: int,
                 image: Surface,
                 constant: bool = False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.constant = constant


class MapElementInGame:
    _sprite: Sprite = None
    _action_type: ActionType = None
    _above_player: bool = False
    additional_sprites: tuple[Sprite] = None

    def __init__(self,
                 sprite: Sprite,
                 action_type: ActionType,
                 additional_sprites: Sprite | tuple[Sprite]):
        self._sprite = sprite
        self._action_type = action_type
        self.additional_sprites = additional_sprites if isinstance(additional_sprites, tuple) else (additional_sprites,)
        if len(self.additional_sprites) > 1:
            self.above_player = True

    @property
    def sprite(self):
        return self._sprite

    @property
    def action_type(self):
        return self._action_type

    @property
    def above_player(self):
        return self._above_player

    @above_player.setter
    def above_player(self, value):
        self.above_player = value
