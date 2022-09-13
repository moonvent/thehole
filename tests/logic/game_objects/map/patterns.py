from src.logic.game_objects.map.location_patterns import Location, Sides

# карта для теста на поход по возвышенностям и на стопы если не по лестнице заход на возвышенность

MoveLocation = Location(pattern=(
        'ggbdddddcggggg',
        'eggeggeggggggg',
        'ggggmjgggggggg',
        'gdgggkgggggggg',
        'gdgggilggggggg',),
    sides=Sides.All,
    next_locations=()
)
