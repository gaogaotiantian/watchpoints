# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import unittest
import inspect
from watchpoints.watch_element import WatchElement
from watchpoints.util import getargnodes


class TestWatchElement(unittest.TestCase):
    def helper(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        argnodes = getargnodes(frame)
        return [WatchElement(
                    frame,
                    node,
                    alias=kwargs.get("alias", None),
                    default_alias=name,
                    printer=kwargs.get("printer", None),
                    callback=kwargs.get("callback", None)
                ) for node, name in argnodes]

    def test_basic(self):
        a = 0
        b = []
        c = {}
        d = set()

        lst = self.helper(a, b,
                          c, d)
        self.assertEqual(len(lst), 4)

    def test_changed(self):
        class MyObj:
            def __init__(self):
                self.a = 0

        a = []
        b = [1, 2]
        c = MyObj()
        frame = inspect.currentframe()
        lst = self.helper(a, b[0], c.a)
        wea = lst[0]
        web = lst[1]
        wec = lst[2]
        c.a = 0
        self.assertFalse(wec.changed(frame)[0])
        a.append(1)
        b[0] = 3
        c.a = 5
        self.assertTrue(wea.changed(frame)[0])
        self.assertTrue(web.changed(frame)[0])
        self.assertTrue(wec.changed(frame)[0])

    def test_same(self):
        a = []
        b = a
        lst = self.helper(a, alias="a")
        self.assertTrue(lst[0].same(a))
        self.assertTrue(lst[0].same(b))
        self.assertTrue(lst[0].same("a"))
        self.assertTrue(lst[0].belong_to([a]))
        self.assertFalse(lst[0].belong_to(["b"]))
