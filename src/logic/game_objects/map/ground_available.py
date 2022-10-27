from src.logic.game_objects.character.mechanics.directions import MoveDirection
from src.logic.game_objects.map.element import MapElementInGame, ElementAvailability
from src.logic.game_objects.map.location_patterns import Literals, lcode


class _GroundAvailable:
    """
        Проверка на возможность ступить на какую-то поверхность С какой-то поверхности, например из реки на сушу и т.д.
    """

    def check_ground_codes(self,
                           next_surface: MapElementInGame,
                           current_surface: MapElementInGame) -> ElementAvailability:
        """
            Проверяем можно ли ступить на след поверхность с текущей, если да - True, если нет - False, если нет след.
                поверхности то None
        :param next_surface:
        :param current_surface:
        :return:
        """

        if not next_surface:
            return ElementAvailability.MapBorder

        # print(self.surfaces_history[-1].code, next_element.code)

        match next_surface.code:
            # проверяем следующий элемент на который ступит игрок с текущим, кейсы рассчитаны на след. элемент,
            # логика в кейсах на текущий

            case Literals.d:
                # хайграунд трава
                return ElementAvailability.Step if current_surface.code in (Literals.b, Literals.d, Literals.c, Literals.l, Literals.m) else ElementAvailability.NoStep

            case Literals.b:
                # подъём вправо
                match current_surface.code:
                    case Literals.g if self.direction == MoveDirection.Right:
                        return ElementAvailability.Step
                    case Literals.b | Literals.d | Literals.j:
                        return ElementAvailability.Step
                    case _:
                        return ElementAvailability.NoStep

            case Literals.c:
                # спуск вправо
                match current_surface.code:
                    case Literals.g if self.direction == MoveDirection.Left:
                        return ElementAvailability.Step
                    case Literals.c | Literals.d | Literals.i:
                        return ElementAvailability.Step
                    case _:
                        return ElementAvailability.NoStep

            case Literals.m:
                match current_surface.code:
                    case Literals.g if self.direction == MoveDirection.Right:
                        return ElementAvailability.Step
                    case Literals.m | Literals.k | Literals.j | Literals.i | Literals.k:
                        return ElementAvailability.Step
                    case _:
                        return ElementAvailability.NoStep

            case Literals.l:
                match current_surface.code:
                    case Literals.g if self.direction == MoveDirection.Left:
                        return ElementAvailability.Step
                    case Literals.l | Literals.k | Literals.j | Literals.i | Literals.k:
                        return ElementAvailability.Step
                    case _:
                        return ElementAvailability.NoStep

            case Literals.g | Literals.e | Literals.f | Literals.s:
                #   обычная земля / ёлки
                return ElementAvailability.Step if current_surface.code in (Literals.b, Literals.c, Literals.g, Literals.e, Literals.l, Literals.m, lcode.f, lcode.s) else ElementAvailability.NoStep

            case Literals.k | Literals.j | Literals.i | Literals.k | Literals.n:
                # длинный хайграунд
                return ElementAvailability.Step if current_surface.code in (Literals.h, Literals.k, Literals.j, Literals.i, Literals.b, Literals.c, Literals.l, Literals.m, Literals.n) else ElementAvailability.NoStep

            case lcode.o | lcode.p | lcode.q | lcode.r:
                # длинный хайграунд
                return ElementAvailability.NoStep
                # return current_surface.code in (Literals.h, Literals.k, Literals.j, Literals.i, Literals.b, Literals.c, Literals.l, Literals.m, Literals.n)
