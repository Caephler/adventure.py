#!python3
"""
string_message_test.py
Tests for StringMessage
"""

import unittest
import re
import adventure


class StringMessageTests(unittest.TestCase):
    """
    StringMessageTests
    Unit Tests for the StringMessage class
    """

    def test_implemented_message_class(self):
        """
        StringMessage should implement the Message abstract class.
        """
        msg = adventure.StringMessage()
        self.assertIsInstance(msg, adventure.Message)

    def test_print(self):
        """
        StringMessage should be able to print in the specified format.
        """
        msg = adventure.StringMessage()
        regex = re.compile(r'\[\d{2}-\d{2}-\d{4} \d{2}:\d{2}\] .*')
        result = regex.match(msg.print())
        self.assertTrue(result)
