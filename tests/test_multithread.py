# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from watchpoints import watch, unwatch
from watchpoints.watch_print import WatchPrint
from contextlib import redirect_stdout
import io
import inspect
import unittest
import threading
import time
import sys


class myThread (threading.Thread):
    def __init__(self, threadID, name, obj):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.obj = obj

    def run(self):
        for i in range(self.threadID * 5, (self.threadID + 1) * 5):
            self.obj[0] = i
            time.sleep(0.001)


class CB:
    def __init__(self):
        self.counter = 0

    def __call__(self, *args):
        self.counter += 1


class TestMultiThraed(unittest.TestCase):
    def test_basic(self):
        cb = CB()
        a = [0]
        watch(a, callback=cb)
        # Create new threads
        thread1 = myThread(1, "Thread-1", a)
        thread2 = myThread(2, "Thread-2", a)

        # Start new Threads
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        unwatch()
        self.assertEqual(cb.counter, 10)

    def test_watch_print(self):
        class Elem:
            def __init__(self):
                self.alias = None
                self.default_alias = "a"
                self.prev_obj = ""
                self.obj = ""

        a = [0]
        # Create new threads
        thread1 = myThread(1, "Thread-1", a)
        thread2 = myThread(2, "Thread-2", a)

        # Start new Threads
        thread1.start()
        thread2.start()

        s = io.StringIO()
        with redirect_stdout(s):
            wp = WatchPrint(file=sys.stdout)
            wp(inspect.currentframe(), Elem(), ("a", "b", "c"))
            self.assertIn("Thread", s.getvalue())

        thread1.join()
        thread2.join()

        unwatch()
