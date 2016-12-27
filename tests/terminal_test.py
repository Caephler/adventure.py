#!python3

import unittest
import adventure


class TerminalTests(unittest.TestCase):
    """
    TerminalTests
    Unit Tests for the Terminal class.
    """

    def test_init(self):
        """
        Terminal should initialize properly.
        """
        term = adventure.Terminal()
        self.assertIsInstance(term, adventure.Terminal)
