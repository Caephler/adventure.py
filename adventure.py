#! python3
"""
adventure.py
------------
simple text adventure game
"""
from abc import ABCMeta, abstractmethod
import time


class Message:
    """
    Message
    Message for terminal output
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def print(self):
        """
        print
        Should return a printable string.
        """
        raise NotImplementedError()


class StringMessage(Message):
    """
    StringMessage
    Basic Message that contains a string as its message.
    """

    def __init__(self, string=""):
        self.msg = string
        self.timestamp = time.localtime()

    def print(self):
        return "[{0}] {1}".format(
            time.strftime("%d-%m-%Y %H:%M", self.timestamp), self.msg)


class MessageList:
    """
    MessageList
    List of messages
    """

    def __init__(self):
        self.__list = []

    def __iter__(self):
        return iter(self.__list)

    def push(self, message):
        """
        MessageList.push(message)
        Appends a Message object at the end of the list.
        """
        if not isinstance(message, Message):
            raise TypeError()
        self.__list.append(message)

    def pop(self, index=None):
        """
        MessageList.pop(index=None)
        Removes element at index from the list.
        If index is not specified, last element is removed.
        Returns element that was popped.
        """
        if index is None:
            if self.length() == 0:
                raise IndexError()
            else:
                index = self.length() - 1
        elif (self.length() == 0) or (index < 0) or (index >= self.length()):
            raise IndexError()

        elem = self.__list[index]
        self.__list = self.__list[0:index] + self.__list[index + 1:]
        return elem

    def length(self):
        """
        MessageList.length()
        Returns number of messages on the list.
        """
        return len(self.__list)


class Terminal:
    """
    Terminal
    All printing should be done through a Terminal instance.
    """

    def __init__(self):
        self.__msg_list = MessageList()

    def push_message(self, string):
        self.__msg_list.push(StringMessage(string))

    def render(self):
        for msg in self.__msg_list:
            print(msg.print())


def main():
    term = Terminal()
    term.push_message("Hello!")
    term.push_message("Hiya!")
    term.render()

if __name__ == "__main__":
    main()
