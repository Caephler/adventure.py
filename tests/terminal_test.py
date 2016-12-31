#!python3

import unittest
import adventure
import adventure_map as amap
import story
import messages


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

    def test_use_story(self):
        """
        Terminal should be able to use a Story object
        to allow the user to start the interactive game
        """
        term = adventure.Terminal()
        self.assertRaises(TypeError, term.use_story, "a")
        self.assertRaises(TypeError, term.use_story, [1, 2])
        term.use_story(story.Story())

    def test_push_string_message(self):
        """
        Terminal should be able to push a StringMessage
        to its internal MessageList object
        """
        term = adventure.Terminal()
        term.push_message("ok")
        self.assertTrue(
            isinstance(term.debug_get_msg_list()[0], messages.StringMessage))

    def test_push_map_message(self):
        """
        Terminal should be able to push a MapMessage
        to its internal MessageList object
        """
        term = adventure.Terminal()
        term.push_map_message(amap.Map([[]]))
        self.assertTrue(
            isinstance(term.debug_get_msg_list()[0], messages.MapMessage)
        )

    def test_push_divider(self):
        """
        Terminal should be able to push a Divider
        to its internal MessageList object
        """
        term = adventure.Terminal()
        term.push_message_divider()
        term.push_message_divider("ok")
        msg_list = term.debug_get_msg_list()
        self.assertTrue(isinstance(msg_list[0], messages.Divider))
        self.assertTrue(isinstance(msg_list[1], messages.Divider))
