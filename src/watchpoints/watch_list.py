# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from .decorator import add_callback
from .watch_print import WatchPrint


class WatchList(list):
    def __init__(self, *args, **kwargs):
        self._callback = WatchPrint("list")
        self._callback_kwargs = {}
        self._alias = kwargs.get("alias", None)
        list.__init__(self, *args, **kwargs)

    @add_callback
    def __setitem__(self, key, value):
        list.__setitem__(self, key, value)

    @add_callback
    def append(self, x):
        list.append(self, x)

    @add_callback
    def extend(self, iterable):
        list.extend(self, iterable)

    @add_callback
    def insert(self, i, x):
        list.insert(self, i, x)

    @add_callback
    def remove(self, x):
        list.remove(self, x)

    @add_callback
    def pop(self, i=-1):
        return list.pop(self, i)

    @add_callback
    def clear(self):
        list.clear(self)

    @add_callback
    def sort(self, *args, key=None, reverse=False):
        list.sort(self, *args, key=key, reverse=reverse)

    @add_callback
    def reverse(self):
        list.reverse(self)

    def set_callback(self, cb, **kwargs):
        self._callback = cb
        self._callback_kwargs = kwargs
