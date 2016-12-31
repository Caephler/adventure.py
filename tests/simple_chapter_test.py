#!python3

import unittest
import story
import messages
import adventure_map as amap
import adventure as adv


class SimpleChapterTests(unittest.TestCase):
    """
    SimpleChapterTests
    Tests for the SimpleChapter class
    """

    def test_init_good_args(self):
        """
        SimpleChapter should initialize with a Map object
        and an optional ChapterObjectives object
        """
        story.SimpleChapter(amap.Map([[]]))
        story.SimpleChapter(amap.Map([[]]), story.ChapterObjectives())

    def test_init_bad_args(self):
        """
        SimpleChapter should not initialize with bad arguments
        """
        self.assertRaises(TypeError, story.SimpleChapter)
        self.assertRaises(TypeError, story.SimpleChapter, 1, 1)
        self.assertRaises(TypeError, story.SimpleChapter, "hello")

    def test_add_subscriber(self):
        """
        SimpleChapter should be able to be subscribed to by a
        Terminal instance, and emitted messages should be read
        by the Terminal instance
        """
        chapter_map = amap.Map([[]])
        chapter = story.SimpleChapter(chapter_map)
        term = adv.Terminal()
        chapter.add_subscriber(term)
        chapter.string_reply("Test message")

    def test_string_reply(self):
        """
        SimpleChapter.string_reply should push a StringMessage
        to all its subscribers
        """
        chapter_map = amap.Map([[]])
        chapter = story.SimpleChapter(chapter_map)
        term = adv.Terminal()
        term2 = adv.Terminal()
        chapter.add_subscriber(term)
        chapter.add_subscriber(term2)
        msg = "Test Message"
        chapter.string_reply(msg)
        self.assertEqual(msg, term.debug_get_msg_list()[0].msg)
        self.assertEqual(msg, term2.debug_get_msg_list()[0].msg)

    def test_map_reply(self):
        """
        SimpleChapter.map_reply should push a MapMessage
        to all its subscribers
        """
        chapter_map = amap.Map([[]])
        chapter = story.SimpleChapter(chapter_map)
        term = adv.Terminal()
        term2 = adv.Terminal()
        chapter.add_subscriber(term)
        chapter.add_subscriber(term2)
        chapter.map_reply()
        self.assertEqual(chapter.map_inst,
                         term.debug_get_msg_list()[0].map)
        self.assertEqual(chapter.map_inst,
                         term2.debug_get_msg_list()[0].map)

    def test_remove_subscriber(self):
        """
        SimpleChapter.rem_subscriber should remove a
        terminal instance which is subscribed to it
        """
        chapter_map = amap.Map([[]])
        chapter = story.SimpleChapter(chapter_map)
        term = adv.Terminal()
        term2 = adv.Terminal()
        chapter.add_subscriber(term)
        chapter.add_subscriber(term2)
        chapter.map_reply()
        self.assertEqual(1, term.debug_get_msg_list().length())
        self.assertEqual(1, term2.debug_get_msg_list().length())
        chapter.rem_subscriber(term)
        chapter.map_reply()
        self.assertEqual(1, term.debug_get_msg_list().length())
        self.assertEqual(2, term2.debug_get_msg_list().length())
        chapter.rem_subscriber(term2)
        chapter.map_reply()
        self.assertEqual(1, term.debug_get_msg_list().length())
        self.assertEqual(2, term2.debug_get_msg_list().length())

    def test_invalid_remove_subscriber(self):
        """
        SimpleChapter.rem_subscriber should throw an exception
        if the terminal instance is not in its subscriber list
        """
        chapter_map = amap.Map([[]])
        chapter = story.SimpleChapter(chapter_map)
        term = adv.Terminal()
        self.assertRaises(ValueError, chapter.rem_subscriber, term)

    def test_player_moves(self):
        """
        SimpleChapter should raise an InvalidMoveError if
        the move is invalid, and move to new position if
        the moving direction is valid.
        """
        a = amap.MapObject("path", ".", True)
        b = amap.MapObject("rock", "X", False)
        chapter_map = amap.Map([
            [a, a, a, a, a],
            [b, a, b, a, b],
            [a, a, b, a, a],
            [b, b, b, b, b]
        ])
        chapter = story.SimpleChapter(chapter_map, [0, 0])
        self.assertRaises(story.InvalidMoveError, chapter.player_move, "west")
        self.assertRaises(story.InvalidMoveError, chapter.player_move, "north")
        self.assertRaises(story.InvalidMoveError, chapter.player_move, "south")
        self.assertEqual(chapter.player_pos, [0, 0])
        chapter.player_move("east")
        chapter.player_move("south")
        self.assertRaises(story.InvalidMoveError, chapter.player_move, "west")
        chapter.player_move("south")
        self.assertRaises(story.InvalidMoveError, chapter.player_move, "south")

    def test_avail_directions(self):
        """
        SimpleChapter should be able to list the available directions the
        player can go, which will only be shown when the player has a torch.
        SimpleChapter.avail_dirs will return the directions in a list in the
        following precedence order - "north", "east", "south", "west"
        """
        a = amap.MapObject("path", ".", True)
        b = amap.MapObject("rock", "X", False)
        Q = amap.MapObject("staircase", "@", True)
        co = story.ChapterObjectives()
        co.add_completion_obj(Q)
        chapter_map = amap.Map([
            [a, a, a, a, a],
            [b, a, b, a, b],
            [a, a, Q, a, a],
            [b, b, b, b, b]
        ])
        chapter = story.SimpleChapter(chapter_map, [0, 0], co)
        self.assertEqual(chapter.avail_dirs(), ["east"])
        chapter.player_move("east")
        self.assertEqual(chapter.avail_dirs(), ["east", "south", "west"])
        chapter.player_move("south")
        self.assertEqual(chapter.avail_dirs(), ["north", "south"])

    def test_chapter_completion(self):
        """
        SimpleChapter should signal completion when player is on the staircases
        The Story object should identify with the designated staircase
        MapObject
        """
        a = amap.MapObject("path", ".", True)
        b = amap.MapObject("rock", "X", False)
        Q = amap.MapObject("staircase", "@", True)
        co = story.ChapterObjectives()
        co.add_completion_obj(Q)
        chapter_map = amap.Map([
            [a, a, a, a, a],
            [b, a, b, a, b],
            [a, a, Q, a, a],
            [b, b, b, b, b]
        ])
        chapter = story.SimpleChapter(chapter_map, [0, 0], co)
        self.assertFalse(chapter.is_complete())
        chapter.player_move("east")
        self.assertFalse(chapter.is_complete())
        chapter.player_move("south")
        self.assertFalse(chapter.is_complete())
        chapter.player_move("south")
        self.assertFalse(chapter.is_complete())
        chapter.player_move("east")
        self.assertTrue(chapter.is_complete())
