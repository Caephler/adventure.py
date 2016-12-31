#!python3

import unittest
import adventure_map as amap


class MapTests(unittest.TestCase):
    """
    MapTests
    Tests for the Map class
    """

    def test_init_with_bad_args(self):
        """
        Map should not initialize with bad arguments
        """
        self.assertRaises(TypeError, amap.Map, "a")
        self.assertRaises(TypeError, amap.Map, [["a", "b"]])

    def test_init_with_good_args(self):
        """
        Map should initialize with good arguments
        """
        a = amap.MapObject("Path", " ", True)
        map1 = amap.Map([[]])
        map2 = amap.Map([[a, a, a], [a, a, a]])

    def test_map_is_indexable_by_coords(self):
        """
        Map should be indexable by a set of coordinates
        """
        a = amap.MapObject("Path", ".", True)
        b = amap.MapObject("Stone", "X", False)
        map_inst = amap.Map([
            [a, a, b, a, a],
            [b, b, b, b, b]
        ])
        self.assertEqual(map_inst[(0, 0)], a)
        self.assertEqual(map_inst[(0, 1)], b)
        self.assertEqual(map_inst[(4, 1)], b)

    def test_map_collision(self):
        """
        Map.check_collision should return True if collision occurs,
        and False if otherwise
        """
        a = amap.MapObject("Path", ".", True)
        b = amap.MapObject("Stone", "X", False)
        map_inst = amap.Map([
            [a, a, b, a, a],
            [a, b, b, b, a]
        ])
        self.assertFalse(map_inst.check_collision([0, 1]))
        self.assertFalse(map_inst.check_collision([4, 0]))
        self.assertTrue(map_inst.check_collision([0, 2]))
        self.assertTrue(map_inst.check_collision([1, 1]))
        self.assertTrue(map_inst.check_collision([-1, 0]))  # Left bound check
        self.assertTrue(map_inst.check_collision([0, -1]))  # Top bound check
        self.assertTrue(map_inst.check_collision([5, 0]))  # Right bound check
        self.assertTrue(map_inst.check_collision([4, 2]))  # Bottom bound check


class MapObjectTests(unittest.TestCase):
    """
    MapObjectTests
    Tests for the MapObject class
    """

    def test_init_with_bad_args(self):
        """
        MapObject should not initialize with bad arguments
        """
        self.assertRaises(TypeError, amap.MapObject, "Dog", 1)
        self.assertRaises(TypeError, amap.MapObject, "Dog", True, True)
        self.assertRaises(ValueError, amap.MapObject, "Rock", "ROCK")

    def test_init_with_good_args(self):
        """
        MapObject should initialize with good arguments
        """
        amap.MapObject("Dog", "1")
        amap.MapObject("Path", " ", True)
        amap.MapObject("", "X", False)

    def test_is_not_passable_if_unspecified(self):
        """
        MapObjects should not be passable if is_passable is unspecified
        """
        obj = amap.MapObject("Rock", "X")
        self.assertFalse(obj.is_passable)
