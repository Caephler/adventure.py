#!python3

import unittest
import adventure_map as amap
import story


class ChapterObjectiveTests(unittest.TestCase):
    """
    ChapterObjectiveTests
    Unit tests for the ChapterObjective class
    """

    def test_is_iterable(self):
        """
        ChapterObjectives should be iterable as a dict
        """
        co = story.ChapterObjectives()
        co_iter = iter(co)

    def test_add_completion(self):
        """
        ChapterObjectives should be able to accept a completion object
        """
        Q = amap.MapObject("stairs", "@", True)
        co = story.ChapterObjectives()
        co.add_completion_obj(Q)
        for key, obj in co.items():
            self.assertEqual("completion", key)
            self.assertEqual(Q, obj)

    def test_add_map(self):
        """
        ChapterObjectives should be able to accept a map object
        """
        M = amap.MapObject("map", "#", True)
        co = story.ChapterObjectives()
        co.add_map_obj(M)
        for key, obj in co.items():
            self.assertEqual("map", key)
            self.assertEqual(M, obj)

    def test_add_torch(self):
        """
        ChapterObjectives should be able to accept a torch object
        """
        T = amap.MapObject("map", "%", True)
        co = story.ChapterObjectives()
        co.add_torch_obj(T)
        for key, obj in co.items():
            self.assertEqual("torch", key)
            self.assertEqual(T, obj)

    def test_add_portals(self):
        """
        ChapterObjectives should be able to accept a list of portal objects
        """
        p1 = amap.MapObject("portal_one", "O", True)
        p2 = amap.MapObject("portal_one", "O", True)
        p3 = amap.MapObject("portal_one", "O", True)
        p4 = amap.MapObject("portal_one", "O", True)
        p5 = amap.MapObject("portal_one", "O", True)
        co = story.ChapterObjectives()
        co.add_portal_objs([p1, p2, p3, p4, p5])
        for key, obj in co.items():
            self.assertEqual("portals", key)
            self.assertEqual(len(obj), 5)

    def test_get_next_portal(self):
        """
        ChapterObjectives.get_next_portal should return the next portal
        in the sequence when given a portal object
        """
        p1 = amap.MapObject("portal_one", "O", True)
        p2 = amap.MapObject("portal_one", "O", True)
        p3 = amap.MapObject("portal_one", "O", True)
        p4 = amap.MapObject("portal_one", "O", True)
        p5 = amap.MapObject("portal_one", "O", True)
        co = story.ChapterObjectives()
        co.add_portal_objs([p1, p2, p3, p4, p5])
        next_portal_refs = []
        for key, portals in co.items():
            self.assertEqual("portals", key)
            for portal in portals:
                if len(next_portal_refs) > 0:
                    self.assertEqual(portal, next_portal_refs[-1])
                next_portal = co.get_next_portal(portal)
                next_portal_refs.append(next_portal)

    def test_check_objectives(self):
        """
        ChapterObjectives.check_objective should return the objective key
        if valid in its internal dictionary
        """
        M = amap.MapObject("map", "#", True)
        T = amap.MapObject("torch", "T", True)
        Q = amap.MapObject("stairs", "@", True)
        co = story.ChapterObjectives()
        co.add_map_obj(M)
        co.add_torch_obj(T)
        co.add_completion_obj(Q)
        self.assertEqual("torch", co.check_objective(T))
        self.assertEqual("completion", co.check_objective(Q))
        self.assertEqual("map", co.check_objective(M))
