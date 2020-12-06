# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import functools
import inspect


def add_callback(func):

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._callback:
            frame = inspect.currentframe().f_back
            self._callback(frame, method=func, local_vars=locals(), when="pre", **self._callback_kwargs)
        ret = func(self, *args, **kwargs)
        if self._callback:
            self._callback(frame, method=func, local_vars=locals(), when="post", **self._callback_kwargs)

        return ret

    return wrapper
