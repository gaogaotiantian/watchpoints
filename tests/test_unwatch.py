# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import unittest
from watchpoints import watch, unwatch


class CB:
    def __init__(self):
        self.counter = 0

    def __call__(self, *args):
        self.counter += 1


class TestUnwatch(unittest.TestCase):
    def test_basic(self):
        cb = CB()
        watch.config(callback=cb)
        a = [1, 2, 3]
        watch(a)
        a[1] = 0
        self.assertEqual(cb.counter, 1)
        unwatch(a)
        a[1] = 1
        self.assertEqual(cb.counter, 1)
        watch(a)
        a[1] = 0
        self.assertEqual(cb.counter, 2)
        unwatch()
        a[1] = 2
        self.assertEqual(cb.counter, 2)

    def test_noargs(self):
        cb = CB()
        watch.config(callback=cb)
        a = [1, 2, 3]
        watch(a)
        a[1] = 0
        self.assertEqual(cb.counter, 1)
        unwatch()
        a[1] = 2
        self.assertEqual(cb.counter, 1)

    def test_alias(self):
        cb = CB()
        watch.config(callback=cb)
        a = [1, 2, 3]
        watch(a, alias="a")
        a[1] = 4
        self.assertEqual(cb.counter, 1)
        unwatch("a")
        a[1] = 5
        self.assertEqual(cb.counter, 1)

    def test_long(self):
        cb = CB()
        watch.config(callback=cb)
        a = [1, 2, 3]
        watch(a)
        a[1] = 0
        self.assertEqual(cb.counter, 1)
        unwatch(a)
        a[1] = 1
        self.assertEqual(cb.counter, 1)
        watch(a)
        a[1] = 0
        self.assertEqual(cb.counter, 2)
        unwatch()
        a[1] = 2
        self.assertEqual(cb.counter, 2)
        watch(a)
        a[1] = 0
        self.assertEqual(cb.counter, 3)
        unwatch()
        a[1] = 2
        self.assertEqual(cb.counter, 3)
        watch(a, alias="a")
        a[1] = 4
        self.assertEqual(cb.counter, 4)
        unwatch("a")
        a[1] = 5
        self.assertEqual(cb.counter, 4)
