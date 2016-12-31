#!python3

from abc import ABCMeta, abstractmethod
import time

import adventure_map as amap

timestamp_format = "%d-%m-%Y %H:%M"


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


class Divider(Message):
    """
    Divider
    A horizontal divider.
    """

    def __init__(self, msg=""):
        divider_length = 20
        fill_length = divider_length - len(msg)
        if fill_length == divider_length:
            self.msg = "-" * divider_length
        else:
            left_pad = int(fill_length / 2)
            right_pad = fill_length - left_pad
            self.msg = "-" * left_pad + msg + "-" * right_pad

    def print(self):
        return self.msg


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
            time.strftime(timestamp_format, self.timestamp), self.msg)


class MapMessage(Message):
    """
    MapMessage
    Message that contains a Map object.
    """

    def __init__(self, adv_map):
        if not isinstance(adv_map, amap.Map):
            raise TypeError()
        self.map = adv_map
        self.timestamp = time.localtime()

    def print(self):
        printable = "[{0}] MAP".format(
            time.strftime(timestamp_format, self.timestamp))
        for line in self.map.map_list:
            printed_line = ' '.join([map_obj.symbol for map_obj in line])
            printable = '\n'.join([printable, printed_line])
        return printable


class MessageList:
    """
    MessageList
    List of messages
    """

    def __init__(self, max_length=20):
        self.__list = []
        self.max_length = max_length

    def __iter__(self):
        return iter(self.__list)

    def __getitem__(self, val):
        return self.__list[val]

    def push(self, message):
        """
        MessageList.push(message)
        Appends a Message object at the end of the list.
        """
        if not isinstance(message, Message):
            raise TypeError()
        if len(self.__list) >= self.max_length:
            self.pop(0)
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
