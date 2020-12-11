# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from contextlib import redirect_stdout
import inspect
import io
import sys
import unittest
from unittest.mock import patch
from watchpoints import watch, unwatch


class CB:
    def __init__(self):
        self.counter = 0

    def __call__(self, *args):
        self.counter += 1


# This is a coverage/unit test for trace func
# Because coverage.py relies on settrace, we can't test trace func with
# coverage in black-box test. We try to simulate the settrace call here
# so we can get some coverage data
class TestTraceFunc(unittest.TestCase):
    def test_trace_func(self):
        # Trick watch to let it think it's on
        cb = CB()
        watch.enable = True
        watch.tracefunc_stack.append(sys.gettrace())
        a = 0
        watch.tracefunc(inspect.currentframe(), "line", None)
        b = []
        watch.tracefunc(inspect.currentframe(), "line", None)
        watch(a)
        watch(b, callback=cb)
        b = 1
        watch.tracefunc(inspect.currentframe(), "line", None)
        self.assertEqual(cb.counter, 1)
        s = io.StringIO()
        with redirect_stdout(s):
            self.file = sys.stdout
            a = 1
            watch.tracefunc(inspect.currentframe(), "line", None)
            self.assertEqual(s.getvalue(), "")

        unwatch(b)
        unwatch()

    def test_unwatch(self):
        # Trick watch to let it think it's on
        watch.enable = True
        watch.tracefunc_stack.append(sys.gettrace())
        a = 0
        watch.tracefunc(inspect.currentframe(), "line", None)
        watch(a)
        unwatch(a)
        self.assertEqual(watch.tracefunc_stack, [])

    def test_not_exist(self):
        class MyObj:
            def __init__(self):
                self.a = 0

        watch.enable = True
        watch.tracefunc_stack.append(sys.gettrace())
        a = {"a": 0}
        watch.tracefunc(inspect.currentframe(), "line", None)
        watch(a["a"])
        a.pop("a")
        watch.tracefunc(inspect.currentframe(), "line", None)
        self.assertEqual(watch.watch_list, [])

        watch(a)
        del a
        watch.tracefunc(inspect.currentframe(), "line", None)
        self.assertEqual(watch.watch_list, [])

        obj = MyObj()
        watch(obj.a)
        delattr(obj, "a")
        watch.tracefunc(inspect.currentframe(), "line", None)
        self.assertEqual(watch.watch_list, [])

        unwatch()
        self.assertEqual(watch.tracefunc_stack, [])

    @patch('builtins.input', return_value="q\n")
    @patch('sys.settrace', return_value=None)
    def test_pdb(self, mock_input, mock_settrace):
        watch.enable = True
        watch.config(pdb=True)
        watch.tracefunc_stack.append(sys.gettrace())
        a = 0
        watch(a)
        watch.tracefunc(inspect.currentframe(), "line", None)
        a = 1
        watch.tracefunc(inspect.currentframe(), "line", None)
        watch.tracefunc(inspect.currentframe(), "line", None)
        unwatch(a)
        watch.restore()
        self.assertEqual(watch.tracefunc_stack, [])
