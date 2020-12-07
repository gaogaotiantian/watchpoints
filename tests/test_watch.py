# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import unittest
from watchpoints import watch, unwatch


class CB:
    def __init__(self):
        self.counter = 0

    def __call__(self, *args):
        self.counter += 1


class TestWatch(unittest.TestCase):
    def test_basic(self):
        cb = CB()
        watch.config(callback=cb)
        a = [1, 2, 3]
        watch(a)
        a[0] = 2
        a.append(4)
        b = a
        b.append(5)
        a = {"a": 1}
        a["b"] = 2

        def change(d):
            d["c"] = 3

        change(a)

        self.assertEqual(cb.counter, 6)
        unwatch()

    def test_subscr(self):
        cb = CB()
        watch.config(callback=cb)
        a = [1, 2, 3]
        watch(a[1])
        a[0] = 2
        a[1] = 3
        self.assertEqual(cb.counter, 1)

        def val(arg):
            return 1

        a[val(3)] = 4
        self.assertEqual(cb.counter, 2)
        unwatch()

        a = {"a": 1}
        watch(a["a"])
        a["a"] = 2
        a["b"] = 3
        self.assertEqual(cb.counter, 3)
