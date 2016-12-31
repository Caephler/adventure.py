#!python3
"""
message_test.py
Tests for Message
"""

import unittest
import messages


class MessageTests(unittest.TestCase):
    """
    MessageTests
    Unit Tests for the Message abstract class
    """

    def test_message_is_abstract_class(self):
        """
        Message methods should not work as it is an abstract class
        """
        msg = messages.Message()
        self.assertRaises(NotImplementedError, msg.print)
