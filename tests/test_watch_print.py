# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from contextlib import redirect_stdout
import io
import inspect
import unittest
import os.path
import sys
from watchpoints.watch_print import WatchPrint


class TestWatchPrint(unittest.TestCase):
    def test_basic(self):
        class Elem:
            def __init__(self):
                self.alias = None
                self.default_alias = "a"
                self.prev_obj = ""
                self.obj = ""
        s = io.StringIO()
        with redirect_stdout(s):
            wp = WatchPrint(file=sys.stdout)
            wp(inspect.currentframe(), Elem(), ("a", "b", "c"))
            self.assertNotEqual(s.getvalue(), "")

        s = io.StringIO()
        with redirect_stdout(s):
            wp = WatchPrint(file=sys.stdout)
            elem = Elem()
            elem.alias = "james"
            wp(inspect.currentframe(), elem, ("a", "b", "c"))
            self.assertIn("james", s.getvalue())

    def test_getsourceline(self):
        wp = WatchPrint()
        line = wp.getsourceline((
            None,
            os.path.join(os.path.dirname(__file__), "data", "watchpoints-0.1.5-py3.8.egg", "watchpoints", "watch_print.py"),
            12
        ))
        self.assertEqual(line, ">   class WatchPrint:")

        line = wp.getsourceline((None, "file/not/exist", 100))
        self.assertEqual(line, "unable to locate the source")
