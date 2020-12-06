# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import unittest
import inspect
from watchpoints.util import getline


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
