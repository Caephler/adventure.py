#! python3
"""
adventure.py
------------
simple text adventure game
"""

import os
import messages
import story
import adventure_map as amap


class Terminal:
    """
    Terminal
    All printing should be done through a Terminal instance.
    """

    def __init__(self):
        self.__msg_list = messages.MessageList(25)
        self.story = None

    def debug_get_msg_list(self):
        """
        debug_get_msg_list
        Should only be used when debugging or testing to retrieve
        the internal MessageList.
        """
        return self.__msg_list

    def push_message_divider(self, msg=""):
        self.__msg_list.push(messages.Divider(msg))

    def push_message(self, string):
        self.__msg_list.push(messages.StringMessage(string))

    def push_map_message(self, _map):
        self.__msg_list.push(messages.MapMessage(_map))

    def use_story(self, story_inst):
        if not isinstance(story_inst, story.Story):
            raise TypeError()
        self.story = story_inst

    def start_story(self):
        if self.story is None:
            raise RuntimeError()
        for index, chapter in enumerate(self.story.chapters):
            chapter.add_subscriber(self)
            chapter.chapter_start()
            chapter.rem_subscriber(self)
        self.push_message("You've completed all the levels!")
        self.render()

    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for msg in self.__msg_list:
            print(msg.print())
