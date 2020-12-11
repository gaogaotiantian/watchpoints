# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from contextlib import redirect_stdout
import inspect
import io
import sys
import unittest
from watchpoints import watch, unwatch


# This is a coverage/unit test for trace func
# Because coverage.py relies on settrace, we can't test trace func with
# coverage in black-box test. We try to simulate the settrace call here
# so we can get some coverage data
class TestTraceFunc(unittest.TestCase):
    def test_trace_func(self):
        # Trick watch to let it think it's on
        watch.enable = True
        watch.tracefunc_stack.append(None)
        a = 0
        watch.tracefunc(inspect.currentframe(), "line", None)
        watch(a)
        s = io.StringIO()
        with redirect_stdout(s):
            self.file = sys.stdout
            a = 1
            watch.tracefunc(inspect.currentframe(), "line", None)
            self.assertEqual(s.getvalue(), "")

        unwatch()
