import pygame
from pygame.surface import Surface

from src.logic.game_objects.character.mechanics.action import ActionType
from src.logic.game_objects.map.element import MapElementInGame
from src.logic.game_objects.map.level import MapLevel
from src.logic.game_objects.map.location_patterns import Literals
from src.logic.game_objects.position import _MapPosition, MoveDirection, Position
import pygame.locals as pg_consts

from src.services.constants import GameConstants


class _Lifting:
    _player_level: MapLevel = MapLevel.Usual

    @property
    def player_level(self):
        return self._player_level

    @player_level.setter
    def player_level(self, lifting_direction: MapLevel):
        if not isinstance(lifting_direction, MapLevel):
            raise ValueError('lifting_direction должно быть "MapLevel" типа')

        self._player_level = lifting_direction

    def change_player_lifting(self,
                              direction: MoveDirection.Left | MoveDirection.Right,
                              surface_level: MapLevel,
                              player_action: ActionType):

        if direction == MoveDirection.Left:
            if player_action == ActionType.lifting_down and surface_level == MapLevel.ElevationUp:
                self.player_level = MapLevel.ElevationUp

            if player_action == ActionType.lifting_up and surface_level == MapLevel.Usual:
                self.player_level = MapLevel.Usual

        else:
            if player_action == ActionType.lifting_down and surface_level == MapLevel.Usual:
                self.player_level = MapLevel.Usual

            if player_action == ActionType.lifting_up and surface_level == MapLevel.ElevationUp:
                self.player_level = MapLevel.ElevationUp


class _ImageMoving:
    _frames_for_walk: list[Surface] = None

    def move_image(self, direction: MoveDirection):

        match direction:

            case MoveDirection.Up:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_back,] * 4 + \
                                           [pygame.transform.flip(self.action_back, True, False),] * 4

                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = MoveDirection.Up

            case MoveDirection.Down:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_front_walk_0,] * 4 + \
                                           [self.action_front_walk_1,] * 4
                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = MoveDirection.Down

            case MoveDirection.Right | MoveDirection.Left:
                if not self._frames_for_walk:
                    self._frames_for_walk = [self.action_walk_0, self.action_walk_1, self.action_walk_2,
                                             self.action_walk_3, self.action_walk_4, self.action_walk_5,
                                             self.action_walk_6, self.action_walk_7,]
                    if direction == MoveDirection.Left:
                        self._frames_for_walk = [pygame.transform.flip(action, True, False) for action in self._frames_for_walk]

                self.image = self._frames_for_walk.pop(0)

                self._last_move_direction = direction

            case MoveDirection.Stop:

                if self._last_move_direction != MoveDirection.Up:

                    image = self.action_side
                    if self._last_move_direction == MoveDirection.Left:
                        image = self.action_flip_side

                    self.image = image


class _PreparingToNextStep:
    """
        Класс в котором расписаны методы просчитывания куда пойдет игрок на один блок,
        для того чтоб не заходил на возвышености
    """
    _last_action: ActionType = None

    @property
    def last_action(self):
        return self._last_action

    @last_action.setter
    def last_action(self, value: ActionType):
        if not isinstance(value, ActionType):
            raise TypeError('"_last_action" должен быть типа "ActionType"')
        self._last_action = value

    def check_available_walk(self,
                             surface: MapElementInGame,
                             current_player_pos: Position,
                             direction: MoveDirection) -> bool:
        """
            Проверка на возможность ходить по поверхности
        :param direction:
        :param surface: поверхность на которой персонаж
        :param current_player_pos: текущая его позиция
        :return: если нельзя - false, иначе - true
        """
        match direction:

            case MoveDirection.Left if surface.code == Literals.b:
                return True

            case MoveDirection.Right if surface.code == Literals.c:
                return True

        if rects_for_walk := surface.available_walk_side:
            for rect_for_walk in rects_for_walk:
                if rect_for_walk.collidepoint(current_player_pos.x,
                                              current_player_pos.y):
                    return True

            else:
                return False

    def check_next_position(self,
                            current_surface: MapElementInGame,
                            direction: MoveDirection) -> bool | None:
        """
            Получение следующего блока, и проверка его на возможность зайти на него
        :param direction: направления куда двигается персонаж
        :param current_surface: текущее место где стоит персонаж
        :return: можно или нет идти на следующий блок, и если следующего блока нет - None
        """
        from src.logic.game_objects.world import map_object

        if not current_surface:
            return False

        current_surace_rect = current_surface.sprite.rect

        x, y = 0, 0
        current_player_pos = Position(self.coords.x - (self.coords.x // GameConstants.WidthMapElement * GameConstants.WidthMapElement),
                                      self.coords.y - (self.coords.y // GameConstants.HeightMapElement * GameConstants.HeightMapElement))

        match direction:

            case MoveDirection.Up if self.rect.top < current_surace_rect.y:
                if current_surface.code in (Literals.b, Literals.c):
                    return False

                x, y = self.rect.centerx, self.rect.bottom - GameConstants.DefaultStepPixels
                if current_player_pos.y > GameConstants.DefaultStepPixels:
                    current_player_pos.y -= GameConstants.DefaultStepPixels

            case MoveDirection.Down if self.rect.bottom > current_surace_rect.y:
                if current_surface.code in (Literals.b, Literals.c):
                    return False

                x, y = self.rect.centerx, self.rect.bottom + GameConstants.DefaultStepPixels
                if current_player_pos.y < GameConstants.HeightMapElement - GameConstants.DefaultStepPixels:
                    current_player_pos.y += GameConstants.DefaultStepPixels

            case MoveDirection.Left if self.rect.left < current_surace_rect.x:
                x, y = self.rect.left, self.rect.bottom
                if current_player_pos.x > GameConstants.DefaultStepPixels:
                    current_player_pos.x -= GameConstants.DefaultStepPixels

            case MoveDirection.Right if self.rect.right > current_surace_rect.x:
                x, y = self.rect.right, self.rect.bottom
                if current_player_pos.x < GameConstants.WidthMapElement - GameConstants.DefaultStepPixels:
                    current_player_pos.x += GameConstants.DefaultStepPixels

        if not self.check_available_walk(surface=current_surface,
                                         current_player_pos=current_player_pos,
                                         direction=direction):
            return False

        if x and y:
            next_element = map_object.get_element_by_coords(x=x,
                                                            y=y)

            if not next_element:
                return None

            if next_element.code == Literals.d and current_surface.code in (Literals.b, Literals.c):
                ...

            # elif next_element.code == current_surface.code == Literals.d:
            #     ...

            # print(self.surfaces_history[-1].code, next_element.code)

            match next_element.code:
                # проверяем следующий элемент на который ступит игрок с текущим, кейсы рассчитаны на след. элемент,
                # логика в кейсах на текущий

                case Literals.d:
                    # хайграунд трава
                    return current_surface.code in (Literals.b, Literals.d, Literals.c, Literals.l, Literals.m)

                case Literals.b:
                    # подъём вправо
                    match current_surface.code:
                        case Literals.g if self.direction == MoveDirection.Right:
                            return True
                        case Literals.b | Literals.d | Literals.j:
                            return True

                case Literals.c:
                    # спуск вправо
                    match current_surface.code:
                        case Literals.g if self.direction == MoveDirection.Left:
                            return True
                        case Literals.c | Literals.d | Literals.i:
                            return True

                case Literals.m:
                    # подъём вправо
                    match current_surface.code:
                        case Literals.g if self.direction == MoveDirection.Right:
                            return True
                        case Literals.m | Literals.k | Literals.j | Literals.i | Literals.k:
                            return True

                case Literals.l:
                    # спуск вправо
                    match current_surface.code:
                        case Literals.g if self.direction == MoveDirection.Left:
                            return True
                        case Literals.l | Literals.k | Literals.j | Literals.i | Literals.k:
                            return True

                case Literals.g | Literals.e:
                    #   обычная земля / ёлки
                    return current_surface.code in (Literals.b, Literals.c, Literals.g, Literals.e, Literals.l, Literals.m)

                case Literals.k | Literals.j | Literals.i | Literals.k:
                    # длинный хайграунд
                    return current_surface.code in (Literals.h, Literals.k, Literals.j, Literals.i, Literals.b, Literals.c, Literals.l, Literals.m)
        else:
            return True


class _Moving(_MapPosition,
              _Lifting,
              _ImageMoving,
              _PreparingToNextStep):
    """
        Класс для перемещения персонажа
    """
    _current_direction: MoveDirection = MoveDirection.Right
    _last_move_direction: MoveDirection = None

    def __init__(self):
        self._surfaces_history = []

    @property
    def direction(self):
        return self._current_direction

    @direction.setter
    def direction(self,
                  new_direction: MoveDirection):
        if not isinstance(new_direction, MoveDirection):
            raise ValueError('new_direction is not "MoveDirection" type')
        self._current_direction = new_direction

    def move_up(self,
                surface: MapElementInGame) -> bool | None:

        self.direction = direction = MoveDirection.Up
        self.last_action = ActionType.usual

        next_position = self.check_next_position(current_surface=surface,
                                                 direction=MoveDirection.Up)
        if next_position:
            self.position_up()
            self.move_image(direction=MoveDirection.Up)

        return next_position

    def move_down(self,
                  surface: MapElementInGame):
        self.direction = direction = MoveDirection.Down
        self.last_action = ActionType.usual

        next_position = self.check_next_position(current_surface=surface,
                                                 direction=MoveDirection.Down)
        if next_position:
            self.position_down()
            self.move_image(direction=MoveDirection.Down)

        return next_position

    def move_left(self,
                  surface: MapElementInGame):
        self.direction = direction = MoveDirection.Left

        next_position = self.check_next_position(current_surface=surface,
                                                 direction=direction)

        if next_position:
            self.position_left()
            self.move_image(direction=direction)

            if surface.action_type != ActionType.usual:
                # из-за того что слева направо - главное направление - инвертируем стороны
                self.last_action = ActionType.lifting_up if self._last_action == ActionType.lifting_down else ActionType.lifting_down

            self.position_lifting(direction=direction,
                                  action_type=surface.action_type)

            self.change_player_lifting(direction=direction,
                                       surface_level=surface.map_level,
                                       player_action=self.last_action)

        return next_position

    def move_right(self,
                   surface: MapElementInGame):
        self.direction = direction = MoveDirection.Right

        next_position = self.check_next_position(current_surface=surface,
                                                 direction=direction)

        if next_position:
            self.position_right()
            self.move_image(direction=direction)

            if surface.action_type != ActionType.usual:
                self.last_action = surface.action_type

            if self.last_action == ActionType.lifting_up and surface.map_level == MapLevel.ElevationUp:
                self.player_level = MapLevel.ElevationUp

            self.position_lifting(direction=direction,
                                  action_type=surface.action_type)

            self.change_player_lifting(direction=direction,
                                       surface_level=surface.map_level,
                                       player_action=self.last_action)

        return next_position

    def stop(self,
             surface: MapElementInGame,
             swap_sprite: bool = True):
        self.position_stop()
        if swap_sprite:
            self.move_image(MoveDirection.Stop)


class PlayerMovingMixin(_Moving):
    """
        Привязка перещмения игрока к перемещению игрока по кнопкам;
    """
    _directions: dict = None

    def __init__(self):
        super().__init__()
        self._directions = {self.move_up: pg_consts.K_UP,
                            self.move_down: pg_consts.K_DOWN,
                            self.move_left: pg_consts.K_LEFT,
                            self.move_right: pg_consts.K_RIGHT,}

    def moving(self,
               surface: MapElementInGame,
               pressed_button: int | None = None) -> bool | None:
        """
            метод расчета и переноса персонажа
        :param surface: место где стоим
        :param pressed_button: нажатая кнопка
        :return: можно или нет пройти на следующее место, если нет следующего элемента - None
        """

        self.add_surface_to_history(new_surface=surface)

        if pressed_button and pressed_button in GameConstants.PlayerMovingButtoms:
            keys = {pressed_button: True}
        else:
            keys = pygame.key.get_pressed()

        if pressed_buttons := tuple(move_method
                                    for move_method, button_id in self._directions.items()
                                    if (isinstance(keys, dict) and keys.get(button_id)) or
                                       (not isinstance(keys, dict) and keys[button_id])):
            return pressed_buttons[0](surface=surface)

        else:
            self.stop(swap_sprite=True,
                      surface=surface)
            return False
