#!python3


class Map:
    """
    Map
    A Map class.
    """

    def __init__(self, map_list):
        """
        Map(map_list ::= 2D list of MapObjects)
        Example:
            a = MapObject("Path", " ", True)
            b = MapObject("Rock", "X", False)
            map_list = [[a, a, a, a, a]
                        [a, b, b, a, b]]
        """
        if isinstance(map_list, list):
            for x in map_list:
                if not isinstance(x, list):
                    raise TypeError()
                else:
                    for o in x:
                        if not isinstance(o, MapObject):
                            raise TypeError()
        else:
            raise TypeError()

        self.map_list = map_list

    def __getitem__(self, coords):
        x = coords[0]
        y = coords[1]
        return self.map_list[y][x]

    def check_collision(self, coord):
        left_bound = -1
        top_bound = -1
        right_bound = len(self.map_list[0])
        bottom_bound = len(self.map_list)

        if coord[0] <= left_bound or coord[0] >= right_bound:
            return True
        if coord[1] <= top_bound or coord[1] >= bottom_bound:
            return True
        obj_at_point = self.map_list[coord[1]][coord[0]]
        if obj_at_point.is_passable is False:
            return True
        return False


class MapObject:
    """
    MapObject
    Object type for Map legends
    """

    def __init__(self, name, symbol, is_passable=False):
        if isinstance(symbol, str) and len(symbol) > 1:
            raise ValueError()
        if not isinstance(symbol, str) or not isinstance(name, str):
            raise TypeError()
        self.name = name
        self.symbol = symbol
        self.is_passable = is_passable
