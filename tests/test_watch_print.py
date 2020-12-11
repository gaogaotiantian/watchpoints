# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from contextlib import redirect_stdout
import io
import unittest
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
            wp(None, Elem(), ("a", "b", "c"))
            self.assertNotEqual(s.getvalue(), "")

        s = io.StringIO()
        with redirect_stdout(s):
            wp = WatchPrint(file=sys.stdout)
            elem = Elem()
            elem.alias = "james"
            wp(None, elem, ("a", "b", "c"))
            self.assertIn("james", s.getvalue())
