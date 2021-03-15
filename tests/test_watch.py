# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from contextlib import redirect_stdout
import io
import sys
import unittest
from watchpoints import watch, unwatch


class CB:
    def __init__(self):
        self.counter = 0

    def __call__(self, *args):
        self.counter += 1


class TestWatch(unittest.TestCase):
    def setUp(self):
        unwatch()
        watch.restore()

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

        with self.assertRaises(ValueError):
            watch(a[0:2])

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

        unwatch()

    def test_attr(self):
        class MyObj:
            def __init__(self):
                self.a = 0

        cb = CB()
        watch.config(callback=cb)
        obj = MyObj()
        watch(obj.a)
        obj.a = 1
        self.assertEqual(cb.counter, 1)
        unwatch(obj.a)
        obj.a = 2
        self.assertEqual(cb.counter, 1)
        watch(obj)
        obj.a = 3
        self.assertEqual(cb.counter, 2)
        obj.a = 3
        self.assertEqual(cb.counter, 2)

    def test_element_callback(self):
        cb = CB()
        a = [1, 2, 3]
        watch(a, callback=cb)
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

    def test_track(self):
        cb = CB()
        a = [1, 2, 3]
        b = [1, 2, 3]
        watch(a, callback=cb, track="object")
        a[0] = 2
        self.assertEqual(cb.counter, 1)
        a = {}
        self.assertEqual(cb.counter, 1)
        watch(b, callback=cb, track=["variable"])
        b[0] = 2
        self.assertEqual(cb.counter, 1)
        b = {}
        self.assertEqual(cb.counter, 2)

        with self.assertRaises(ValueError):
            c = []
            watch(c, track=["invalid"])

        with self.assertRaises(ValueError):
            c = []
            watch(c, track="invalid")

        with self.assertRaises(ValueError):
            c = []
            watch(c, track=[])

        with self.assertRaises(TypeError):
            c = []
            watch(c, track={})

        unwatch()

    def test_when(self):
        cb = CB()
        a = 0
        watch(a, callback=cb, when=lambda x: x > 0)
        a = -1
        a = 1
        a = 2
        a = -3
        self.assertEqual(cb.counter, 2)
        unwatch()

    def test_deepcopy(self):
        cb = CB()
        a = {"a": [0]}
        watch(a, callback=cb)
        a["a"][0] = 1
        self.assertEqual(cb.counter, 0)
        unwatch()
        watch(a, callback=cb, deepcopy=True)
        a["a"][0] = 2
        self.assertEqual(cb.counter, 1)
        unwatch()

    def test_custom_copy(self):

        def copy(obj):
            return {"a": 0}

        cb = CB()
        a = {"a": 0}
        watch(a, callback=cb, copy=copy)
        a["a"] = 1
        self.assertEqual(cb.counter, 1)
        a["a"] = 1
        self.assertGreater(cb.counter, 2)
        unwatch()

    def test_custom_cmp(self):

        def cmp(obj1, obj2):
            return False

        cb = CB()
        a = {"a": 0}
        watch(a, callback=cb, cmp=cmp)
        a["a"] = 1
        self.assertEqual(cb.counter, 0)
        a["a"] = 2
        self.assertEqual(cb.counter, 0)
        unwatch()

    def test_install(self):
        watch.install("_watch")
        _watch()  # noqa
        cb = CB()
        a = [1, 2, 3]
        watch(a, callback=cb)
        a[0] = 2
        self.assertEqual(cb.counter, 1)
        _watch.unwatch()  # noqa
        watch.uninstall("_watch")
        with self.assertRaises(NameError):
            _watch(a)  # noqa

    def test_printer(self):
        s = io.StringIO()
        with redirect_stdout(s):
            watch.config(file=sys.stdout)
            a = [1, 2, 3]
            watch(a)
            a[0] = 2
            unwatch()
            self.assertNotEqual(s.getvalue(), "")

    def test_stack_limit_global(self):
        watch.config(stack_limit=1)
        s = io.StringIO()
        with redirect_stdout(s):
            watch.config(file=sys.stdout)
            a = [1, 2, 3]
            watch(a)
            a[0] = 2
            unwatch()
            self.assertEqual(s.getvalue().count("> "), 1)

    def test_stack_limit_local(self):
        s = io.StringIO()
        with redirect_stdout(s):
            a = [1, 2, 3]
            watch(a, file=sys.stdout, stack_limit=1)
            a[0] = 2
            unwatch()
            self.assertEqual(s.getvalue().count("> "), 1)

    def test_write_to_file(self):
        f = open("tmp_test.log", "w")
        a = [1, 2, 3]
        watch(a, file=f, stack_limit=1)
        a[0] = 2
        unwatch()
        f.close()
        with open("tmp_test.log") as f:
            data = f.read()
        self.assertEqual(data.count("> "), 1)
