#!python3


class Map:
    """
    Map
    A Map class.
    """

    def __init__(self, map_list, legend):
        """
        Map(map_list ::= 2D list, legend ::= dictionary)
        Example:
            map_list = [[0, 0, 0, 0, 0]
                        [0, 1, 0, 1, 0]]
            legend = {
                0: "path",
                1: "block"
            }
        """
        if isinstance(map_list, list):
            for x in map_list:
                if not isinstance(x, list):
                    raise ValueError()
        else:
            raise ValueError()

        if not isinstance(legend, dict):
            raise ValueError()
        self.map_list = map_list
        self.legend = legend
