from logic.game_objects.action import ActionType
from pygame.sprite import Sprite
from pygame.surface import Surface


class MapElement(Sprite):

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


class MapElementInGame:
    _sprite: Sprite = None
    _action_type: ActionType = None
    additional_sprites: tuple = None

    def __init__(self,
                 sprite: Sprite,
                 action_type: ActionType,
                 additional_sprites: Sprite | tuple[Sprite]):
        self._sprite = sprite
        self._action_type = action_type
        self.additional_sprites = additional_sprites if isinstance(additional_sprites, tuple) else (additional_sprites,)

    @property
    def Sprite(self):
        return self._sprite

    @property
    def ActionType(self):
        return self._action_type
