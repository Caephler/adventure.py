#!python3
"""
message_test.py
Tests for Message
"""

import unittest
import adventure


class MessageTests(unittest.TestCase):
    """
    MessageTests
    Unit Tests for the Message abstract class
    """

    def test_message_is_abstract_class(self):
        """
        Message is an abstract class; should not be able to call any methods on it.
        """
        msg = adventure.Message()
        self.assertRaises(NotImplementedError, msg.print)
