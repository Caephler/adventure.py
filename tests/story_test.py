#!python3

import unittest
import story


class StoryTests(unittest.TestCase):
    """
    StoryTests
    Unit tests for the Story class
    """

    def test_init(self):
        """
        Story should be able to initialize without arguments
        """
        s = story.Story()
