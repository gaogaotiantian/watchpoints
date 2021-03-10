# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import unittest
import inspect
import sys
from watchpoints.util import getline, getargnodes


class TestUtil(unittest.TestCase):
    def test_getline(self):
        def watch(*args):
            frame = inspect.currentframe().f_back
            return getline(frame)

        a = []
        b = {}
        line = watch(a)
        self.assertEqual(line, "line = watch ( a )")
        line = watch(
            a,
            b
        )
        self.assertEqual(line, "line = watch ( a , b )")

    @unittest.skipIf(sys.platform == "win32", "windows is not supported")
    def test_getline_with_interpreter(self):

        class FakeCode:
            def __init__(self):
                self.co_filename = "<stdin>"

        class FakeFrame:
            def __init__(self):
                self.f_lineno = 1
                self.f_code = FakeCode()

        frame = FakeFrame()
        import readline
        readline.add_history("watch(a)")
        line = getline(frame)
        self.assertEqual(line, "watch(a)")

    def test_getargnodes(self):
        def watch(*args):
            frame = inspect.currentframe().f_back
            return list(getargnodes(frame))

        a = [0, 1]
        b = {}
        argnodes = watch(a)
        self.assertEqual(len(argnodes), 1)
        self.assertEqual(argnodes[0][1], "a")
        argnodes = watch(
            a,
            b
        )
        self.assertEqual(len(argnodes), 2)
        self.assertEqual(argnodes[0][1], "a")
        self.assertEqual(argnodes[1][1], "b")
        argnodes = watch(
            a[0],  # comments
            b
        )
        self.assertEqual(len(argnodes), 2)
        self.assertEqual(argnodes[0][1], "a[0]")
        self.assertEqual(argnodes[1][1], "b")

        with self.assertRaises(Exception):
            argnodes = [i for i in watch(a)]
