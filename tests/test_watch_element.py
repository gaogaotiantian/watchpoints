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
                    default_alias=name,
                    **kwargs
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
        lst = self.helper(c)
        wec = lst[0]
        c.a = 5
        self.assertFalse(wec.changed(frame)[0])
        c.a = 6
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

    def test_track(self):
        a = []
        b = [1, 2]
        frame = inspect.currentframe()
        lst = self.helper(a, track="variable")
        wea = lst[0]
        lst = self.helper(b, track="object")
        web = lst[0]
        a.append(1)
        self.assertFalse(wea.changed(frame)[0])
        a = {}
        self.assertTrue(wea.changed(frame)[0])
        b[0] = 3
        self.assertTrue(web.changed(frame)[0])
        web.update()
        b = {}
        self.assertFalse(web.changed(frame)[0])

    def test_when(self):
        a = [0]
        lst = self.helper(a, when=lambda x: x[0] > 0)
        wea = lst[0]
        self.assertFalse(wea.when(wea.obj))
        a[0] = 1
        self.assertTrue(wea.when(wea.obj))

    def test_deepcopy(self):
        frame = inspect.currentframe()
        a = {"a": [1, 2]}
        lst = self.helper(a)
        wea = lst[0]
        a["a"][0] = 3
        self.assertFalse(wea.changed(frame)[0])
        a = {"a": [1, 2]}
        lst = self.helper(a, deepcopy=True)
        wea = lst[0]
        a["a"][0] = 3
        self.assertTrue(wea.changed(frame)[0])

    def test_custom_cmp(self):

        def cmp(obj1, obj2):
            return False

        frame = inspect.currentframe()
        a = {"a": 1}
        lst = self.helper(a, cmp=cmp)
        wea = lst[0]
        a["a"] = 0
        self.assertFalse(wea.changed(frame)[0])

    def test_custom_copy(self):

        def copy(obj1):
            return {"a": 0}

        frame = inspect.currentframe()
        a = {"a": 1}
        lst = self.helper(a, copy=copy)
        wea = lst[0]
        a["a"] = 0
        self.assertFalse(wea.changed(frame)[0])

        a["a"] = 1
        self.assertTrue(wea.changed(frame)[0])

    def test_object(self):
        class MyObj:
            def __init__(self):
                self.a = {"a": 1}

        class MyObjWithEq:
            def __init__(self):
                self.a = {"a": 1}

            def __eq__(self, other):
                return self.a == other.a

        obj = MyObj()
        obj_eq = MyObjWithEq()
        frame = inspect.currentframe()

        lst = self.helper(obj, obj_eq)
        wobj = lst[0]
        wobj_eq = lst[1]
        obj.a["a"] = 2
        self.assertFalse(wobj.changed(frame)[0])
        obj_eq.a["a"] = 2
        self.assertFalse(wobj_eq.changed(frame)[0])

        lst = self.helper(obj, obj_eq, deepcopy=True)
        wobj = lst[0]
        wobj_eq = lst[1]
        obj.a["a"] = 3
        with self.assertRaises(NotImplementedError):
            wobj.changed(frame)[0]
        obj_eq.a["a"] = 3
        self.assertTrue(wobj_eq.changed(frame)[0])

    def test_invalid(self):
        a = [1, 2, 3]
        with self.assertRaises(ValueError):
            self.helper(a[0:2])

        with self.assertRaises(ValueError):
            self.helper(a, track=[])

        with self.assertRaises(ValueError):
            self.helper(a, track=["invalid"])

        with self.assertRaises(ValueError):
            self.helper(a, track="invalid")

        with self.assertRaises(TypeError):
            self.helper(a, track=123)
