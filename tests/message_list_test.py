#!python3

import unittest
import messages


class MessageListTests(unittest.TestCase):
    """
    MessageListTests
    Unit Tests for the MessageList class
    """

    def test_init(self):
        """
        MessageList should initialize properly.
        """
        msg_list = messages.MessageList()
        msg_list_2 = messages.MessageList(25)
        self.assertIsInstance(msg_list, messages.MessageList)
        self.assertIsInstance(msg_list_2, messages.MessageList)

    def test_initial_length_equals_zero(self):
        """
        MessageList should have an initial length of 0.
        """
        msg_list = messages.MessageList()
        self.assertEqual(msg_list.length(), 0)

    def test_push(self):
        """
        MessageList.push(object) should only work with Message objects.
        """
        msg_list = messages.MessageList()
        self.assertRaises(TypeError, msg_list.push, "a message string")
        msg_list.push(messages.Message())
        self.assertEqual(msg_list.length(), 1)

    def test_pop_no_args(self):
        """
        MessageList.pop() should work without any arguments
        """
        msg_list = messages.MessageList()
        # Adds 5 Message objects to the list.
        msg_list.push(messages.StringMessage("a"))
        msg_list.push(messages.StringMessage("b"))
        msg_list.push(messages.StringMessage("c"))
        msg_list.push(messages.StringMessage("d"))
        msg_list.push(messages.StringMessage("e"))

        self.assertEqual(msg_list.length(), 5)
        popped = msg_list.pop()
        self.assertEqual(msg_list.length(), 4)
        self.assertEqual(popped.msg, "e")
        msg_list.pop()
        msg_list.pop()
        msg_list.pop()
        msg_list.pop()
        self.assertRaises(IndexError, msg_list.pop)

    def test_pop_bad_index(self):
        """
        MessageList should not work with bad index arguments.
        """
        msg_list = messages.MessageList()

        # Adds 3 Message objects to the list.
        msg_list.push(messages.StringMessage("a"))
        msg_list.push(messages.StringMessage("b"))
        msg_list.push(messages.StringMessage("c"))

        self.assertEqual(msg_list.length(), 3)
        self.assertRaises(IndexError, msg_list.pop, 3)
        self.assertRaises(IndexError, msg_list.pop, -1)

    def test_pop_good_index(self):
        """
        MessageList should work with good index arguments
        """
        msg_list = messages.MessageList()

        # Adds 3 Message objects to the list.
        msg_list.push(messages.StringMessage("a"))
        msg_list.push(messages.StringMessage("b"))
        msg_list.push(messages.StringMessage("c"))

        self.assertEqual(msg_list.length(), 3)
        self.assertEqual("b", msg_list.pop(1).msg)
        self.assertEqual("a", msg_list.pop(0).msg)
        self.assertEqual("c", msg_list.pop(0).msg)

    def test_is_iterable(self):
        """
        MessageList should be iterable.
        """
        msg_list = messages.MessageList()

        # Adds 3 Message objects to the list.
        msg_list.push(messages.StringMessage("a"))
        msg_list.push(messages.StringMessage("b"))
        msg_list.push(messages.StringMessage("c"))

        self.assertEqual(["ab", "bb", "cb"], [x.msg + "b" for x in msg_list])
