class Literals:
    a = 'a'
    b = 'b'
    c = 'c'
    d = 'd'
    e = 'e'
    f = 'f'
    g = 'g'
    h = 'h'
    i = 'i'
    j = 'j'
    k = 'k'
    l = 'l'
    m = 'm'
    # a = 'a'
    # a = 'a'
    # a = 'a'
    # a = 'a'
    # a = 'a'
    # a = 'a'
    # a = 'a'
    # a = 'a'
    # a = 'a'


class Sides:
    """
        стороны в которые можно пройти, начиная всегда с левой
    """

    All = (True,) * 4
    Left = (True, ) + (False,) * 3
    Top = (False, True, False, False)
    Right = (False, False, True, False)
    Buttom = (False,) * 3 + (True, )
    RightBottom = (False, False, True, True)


class Location:
    _pattern: tuple[str, ...] = None
    _available_sides: tuple[bool, bool, bool, bool] = None

    def __init__(self,
                 pattern: tuple[str, ...],
                 sides: tuple[bool, bool, bool, bool]):
        self._pattern = pattern
        self._available_sides = sides

    @property
    def pattern(self):
        return self._pattern

    @property
    def available_sides(self):
        return self._available_sides


class Locations:
    """
        Locations in game, all locations have a 14 columns and 5 rows
    """
    _locations: tuple[Location] = None

    def __init__(self,
                 locations: tuple[Location, ...]):
        self._locations = locations

    @property
    def locations(self):
        return self._locations

    def __getitem__(self, item: int) -> Location:
        return self._locations[item]


locations = Locations(locations=(
        Location(pattern=(
            'ggbdddddcggggg',
            'eggeggeggggggg',
            'ggggmjgggggggg',
            'gdgggkgggggggg',
            'gdgggilggggggg',
        ), sides=Sides.RightBottom),
    )
)
