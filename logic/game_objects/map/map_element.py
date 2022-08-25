from logic.game_objects.action import ActionType
from pygame.sprite import Sprite
from pygame.surface import Surface


class MapElement(Sprite):

    def __init__(self,
                 x: int,
                 y: int,
                 image: Surface):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MapElementInGame:
    _sprite: Sprite = None
    _action_type: ActionType = None

    def __init__(self,
                 sprite: Sprite,
                 action_type: ActionType):
        self._sprite = sprite
        self._action_type = action_type

    @property
    def Sprite(self):
        return self._sprite

    @property
    def ActionType(self):
        return self._action_type
