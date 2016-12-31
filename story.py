#!python3

import sys
import random
import adventure_map as amap
import messages


class InvalidMoveError(Exception):
    """
    InvalidMoveError
    Error when player move is invalid
    """

    def __init__(self, dir_name, reason):
        self.dir_name = dir_name
        self.reason = reason


class Story:
    """
    Story
    Mastermind of the game plot
    """

    def __init__(self):
        o = amap.MapObject("path", ".", True)
        x = amap.MapObject("stone", "X", False)
        M = amap.MapObject("map", "M", True)
        T = amap.MapObject("torch", "T", True)
        C = amap.MapObject("confetti", "C", True)
        P = amap.MapObject("portal", "P", True)
        Q = amap.MapObject("stairs", "@", True)
        a = amap.MapObject("portal_one", "O", True)
        b = amap.MapObject("portal_two", "O", True)
        c = amap.MapObject("portal_thr", "O", True)
        d = amap.MapObject("portal_fou", "O", True)
        e = amap.MapObject("portal_fiv", "O", True)

        easy_chapter_obj = ChapterObjectives()
        easy_chapter_obj.add_completion_obj(Q)
        easy_chapter_obj.add_map_obj(M)
        easy_chapter_obj.add_torch_obj(T)
        easy_chapter_obj.add_confetti_obj(C)
        easy_chapter_obj.add_portal_objs([a, b])

        self.chapters = [
            SimpleChapter(
                amap.Map([
                    [M, o, x, o, Q],
                    [x, T, x, o, x],
                    [o, o, x, o, o],
                    [o, x, x, x, o],
                    [o, o, o, o, o],
                ]), chapter_obj=easy_chapter_obj
            ),
            SimpleChapter(
                amap.Map([
                    [M, b, o, o, C],
                    [a, x, x, x, o],
                    [o, x, o, o, o],
                    [o, x, x, o, x],
                    [T, x, Q, o, o],
                ]), chapter_obj=easy_chapter_obj
            ), SimpleChapter(
                amap.Map([
                    [o, o, o, o, o, x],
                    [o, x, o, x, o, x],
                    [x, o, x, x, o, T],
                    [x, o, x, x, x, o],
                    [x, o, x, x, M, C],
                    [b, a, T, o, C, o],
                ]), start=[4, 4], chapter_obj=easy_chapter_obj)]


class ChapterObjectives:
    """
    ChapterObjectives
    A dict wrapper that has a key/value pair for every
    defined objective object
    """

    def __init__(self):
        self.__dict = {}

    def __iter__(self):
        return iter(self.__dict)

    def __getitem__(self, val):
        return self.__dict[val]

    def items(self):
        return self.__dict.items()

    def add_completion_obj(self, obj):
        self.__dict["completion"] = obj

    def add_map_obj(self, obj):
        self.__dict["map"] = obj

    def add_torch_obj(self, obj):
        self.__dict["torch"] = obj

    def add_confetti_obj(self, obj):
        self.__dict["confetti"] = obj

    def add_portal_objs(self, portal_objs):
        """
        # Portals work in this way:
        # In the order defined:
        # Portal 1 -> Portal 2
        # Portal 2 -> Portal 3
        # ...
        # Portal n -> Portal 1
        # Where n is the last portal in array
        """
        self.__dict["portals"] = portal_objs

    def get_next_portal(self, portal_obj):
        portals = self.__dict["portals"]
        index = portals.index(portal_obj)
        next_portal_obj = portals[(index + 1) % len(portals)]
        return next_portal_obj

    def check_objective(self, obj_at_pos):
        """
        check_objectives
        Should check if a position has an objective
        and returns the key for whatever objective it is
        """
        try:
            self.__dict["portals"].index(obj_at_pos)
            return "portal"
        except ValueError:  # object is not a portal
            pass
        except KeyError:  # portals key isn't created yet
            pass
        if obj_at_pos in self.__dict.values():
            for key, obj in self.__dict.items():
                if obj_at_pos is obj:
                    return key
        return None


class SimpleChapter:
    """
    SimpleChapter
    A chapter of the Story that only requires the player
    to get from the start point to the completion object
    """
    cuss_words = ["fuck", "shit", "fuk", "shiet", "cb"]

    def __init__(self, map_inst, start=[0, 0], chapter_obj=None):
        if not isinstance(map_inst, amap.Map):
            raise TypeError()
        self.map_inst = map_inst
        self.player_pos = start
        self.chapter_obj = chapter_obj
        self.subscribers = []
        self.has_torch = False
        self.turn_count = 1

    def add_subscriber(self, terminal):
        import adventure as adv
        if not isinstance(terminal, adv.Terminal):
            raise TypeError()
        self.subscribers.append(terminal)

    def rem_subscriber(self, terminal):
        import adventure as adv
        if not isinstance(terminal, adv.Terminal):
            raise TypeError()
        self.subscribers.remove(terminal)

    def divider_reply(self, msg=""):
        for subscr in self.subscribers:
            subscr.push_message_divider(msg)

    def string_reply(self, msg):
        for subscr in self.subscribers:
            subscr.push_message(msg)

    def map_reply(self):
        for subscr in self.subscribers:
            subscr.push_map_message(self.map_inst)

    def subscriber_render(self):
        for subscr in self.subscribers:
            subscr.render()

    def is_complete(self):
        if self.map_inst[self.player_pos] == self.chapter_obj["completion"]:
            return True
        return False

    def event_check(self):
        if self.chapter_obj is not None:
            pos = self.player_pos
            obj_at_pos = self.map_inst[pos]
            key = self.chapter_obj.check_objective(obj_at_pos)
            if key is None:
                return
            if key == "portal":
                self.string_reply("You step into a portal. Whoa!")
                next_portal = self.chapter_obj.get_next_portal(obj_at_pos)
                for i, row in enumerate(self.map_inst.map_list):
                    try:
                        j = row.index(next_portal)
                        self.player_pos = [j, i]
                        self.string_reply(
                            "You find yourself in a different place...")
                        break
                    except ValueError:
                        pass
            elif key == "completion":
                self.string_reply("You've completed this level!")
                self.string_reply("Moving on...")
            elif key == "map":
                self.string_reply("You found a map lying on the floor!")
                self.map_reply()
            elif key == "torch":
                self.string_reply("You find a torch.")
                if self.has_torch:
                    self.string_reply("But you already have one!")
                else:
                    self.string_reply(
                        "You find a torch. You take it along with you.")
                    self.has_torch = True
            elif key == "confetti":
                self.string_reply("You find some confetti on the floor. Yay!")

    def chapter_start(self):
        self.divider_reply()
        self.string_reply("You wake up in a dark dungeon.")
        while True:
            complete = self.turn_start()
            if complete:
                break

    def turn_start(self):
        self.divider_reply("TURN {}".format(self.turn_count))
        self.event_check()
        if self.has_torch:
            self.string_reply("With your torch, you are able to see better.")
            self.string_reply("You have a few choices of directions:")
            self.string_reply(
                ', '.join([d.capitalize() for d in self.avail_dirs()]))
        else:
            self.string_reply("It's dark. You can't see anything.")
        self.string_reply("Which direction do you move in?")
        self.subscriber_render()
        player_input = input()
        try:
            if player_input == "exit":
                self.string_reply("An escape route appears - how convenient!")
                self.string_reply("See you next time!")
                sys.exit()
            elif player_input in self.cuss_words:
                self.string_reply(' '.join((
                    "How rude!",
                    "A magical genie appears out of nowhere",
                    "and sends you flying in a random direction")))
                player_input = random.choice(self.avail_dirs())
            self.player_move(player_input.lower())
            self.string_reply("You move {}.".format(player_input.lower()))
            if self.is_complete():
                self.string_reply("You found the exit!")
                self.string_reply(
                    "You completed this level in {} turns."
                    .format(self.turn_count))
                return True
            self.turn_count += 1
        except InvalidMoveError as err:
            self.string_reply("Could not move to the {0} because {1}"
                              .format(err.dir_name, err.reason))
        return False

    def avail_dirs(self):
        avail_dir_list = []
        coord = list(self.player_pos)
        w = self.map_inst.check_collision(
            [i1 + i2 for i1, i2 in zip(coord, [-1, 0])])  # West
        e = self.map_inst.check_collision(
            [i1 + i2 for i1, i2 in zip(coord, [1, 0])])  # East
        s = self.map_inst.check_collision(
            [i1 + i2 for i1, i2 in zip(coord, [0, 1])])  # South
        n = self.map_inst.check_collision(
            [i1 + i2 for i1, i2 in zip(coord, [0, -1])])  # North
        if not n:
            avail_dir_list.append("north")
        if not e:
            avail_dir_list.append("east")
        if not s:
            avail_dir_list.append("south")
        if not w:
            avail_dir_list.append("west")
        return avail_dir_list

    def player_move(self, dir_name):
        move_to = list(self.player_pos)
        if dir_name == "west":
            move_to[0] -= 1
        elif dir_name == "east":
            move_to[0] += 1
        elif dir_name == "north":
            move_to[1] -= 1
        elif dir_name == "south":
            move_to[1] += 1
        else:
            raise InvalidMoveError(
                dir_name, ' '.join((
                    "a snake bites you because",
                    "that's an invalid direction"
                )))
        if self.map_inst.check_collision(move_to) is True:
            # Collision occurred, this move is invalid
            raise InvalidMoveError(dir_name, "a collision occurred")
        else:
            self.player_pos = list(move_to)
