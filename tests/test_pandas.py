# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import unittest
from watchpoints import unwatch, watch

try:
    import pandas as pd
    NO_PANDAS = False
except ImportError:
    NO_PANDAS = True


class CB:
    def __init__(self):
        self.counter = 0

    def __call__(self, *args):
        self.counter += 1


@unittest.skipIf(
    NO_PANDAS, reason="You need to install pandas. (pip install pandas)"
)
class TestPandas(unittest.TestCase):
    def test_series(self):
        def __comparison_series__(obj1, obj2):
            return not obj1.equals(obj2)

        cb = CB()

        ss = pd.Series(data=[1, 2, 3], index=list("abc"))

        watch(ss, cmp=__comparison_series__, callback=cb)

        # Should watch here
        self.assertEqual(cb.counter, 0)

        ss.loc["a"] = 10

        self.assertEqual(cb.counter, 1)

        unwatch()

    def test_dataframe_cmp(self):
        def __comparison_dataframe__(obj1, obj2):
            return not obj1.equals(obj2)

        cb = CB()

        df = pd.DataFrame(
            data=[[1, 2], [3, 4], [5, 6]], index=list("abc"), columns=list("AB")
        )

        watch(df, cmp=__comparison_dataframe__, callback=cb)

        # Other stuff happens
        a = 2
        _ = a + 5

        self.assertEqual(cb.counter, 0)

        df.loc["a", "B"] = 10

        self.assertEqual(cb.counter, 1)

        unwatch()

    def test_dataframe(self):
        cb = CB()

        df = pd.DataFrame(
            data=[[1, 2], [3, 4], [5, 6]], index=list("abc"), columns=list("AB")
        )

        watch(df)

        # Other stuff happens
        a = 2
        _ = a + 5

        self.assertEqual(cb.counter, 0)

        df.loc["a", "B"] = 10

        self.assertEqual(cb.counter, 1)

        unwatch()
