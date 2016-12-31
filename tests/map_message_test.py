#!python3

import re
import unittest
import messages
import adventure_map as amap


class MapMessageTests(unittest.TestCase):
    """
    MapMessageTests
    Test class for the MapMessage class
    """

    def test_init_with_good_args(self):
        """
        MapMessage should initialize with good arguments
        """
        a = amap.MapObject("Path", " ", True)
        messages.MapMessage(amap.Map([[]]))
        messages.MapMessage(amap.Map([[a, a, a]]))

    def test_init_with_bad_args(self):
        """
        MapMessage should not initialize with bad arguments
        """
        self.assertRaises(TypeError, messages.MapMessage)
        self.assertRaises(TypeError, messages.MapMessage, [1, 2])
        self.assertRaises(TypeError, messages.MapMessage, {"1": "Rock"})

    def test_print_format(self):
        """
        MapMessage should print a multi-line message in the following format.
        [{timestamp}] MAP
        [ @ @ @ ]
        [ @ @ @ ]
        [ @ @ @ ]
        Where @ represents the corresponding MapObject symbol.
        """
        a = amap.MapObject("Path", " ", True)
        msgobj = messages.MapMessage(amap.Map([[a, a, a]]))
        regex = re.compile(r'\[.*\] MAP\n(\[ .* \])*')
        result = regex.match(msgobj.print())
        self.assertIsNotNone(result)
