# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import unittest
from watchpoints.watch_list import WatchList


class TestWatchList(unittest.TestCase):
    def test_setitem(self):
        wl = WatchList([1, 2, 3])
        wl[0] = 2
        self.assertEqual(wl, [2, 2, 3])

    def test_callback(self):

        def callback(frame, method, local_vars, when, arg):
            arg["test"] += 1

        counter = {"test": 0}

        wl = WatchList([1, 2, 3])
        wl.set_callback(callback, arg=counter)
        wl[0] = 2
        wl.append(3)
        wl.extend([4, 5])
        wl.insert(1, 2)
        wl.remove(5)
        elm = wl.pop()
        self.assertEqual(elm, 4)
        elm = wl.pop(0)
        self.assertEqual(elm, 2)
        wl.sort()
        wl.reverse()
        self.assertEqual(wl, [3, 3, 2, 2])
        wl.clear()
        self.assertEqual(wl, [])
        self.assertEqual(counter["test"], 20)

    def test_print(self):
        wl = WatchList([1, 2, 3])
        wl[0] = 2
        wl.append(3)
        wl.extend([4, 5])
        wl.insert(1, 2)
        wl.remove(5)
        elm = wl.pop()
        self.assertEqual(elm, 4)
        elm = wl.pop(0)
        self.assertEqual(elm, 2)
        wl.sort()
        wl.reverse()
        self.assertEqual(wl, [3, 3, 2, 2])
        wl.clear()
        self.assertEqual(wl, [])
