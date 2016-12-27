#!python3

import unittest
import story


class MapTests(unittest.TestCase):
    """
    MapTests
    Tests for the Map class
    """

    def test_init_with_bad_args(self):
        """
        Map should not initialize with bad arguments
        """
        self.assertRaises(ValueError, story.Map, "a", 2)
        self.assertRaises(ValueError, story.Map, [[1]], [])

    def test_init_with_good_args(self):
        """
        Map should initialize with good arguments
        """
        map = story.Map([[]], {})
        map2 = story.Map([[1, 2, 3], [2, 3, 4]], {
                         1: "path", 2: "gravel", 3: "stone", 4: "mud"
                         })
