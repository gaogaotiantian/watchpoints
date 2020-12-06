# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import inspect
from .ast_monkey import ast_transform
from .util import getargnodes
from .watch_list import WatchList


class Watch:
    def __call__(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        argnodes = getargnodes(frame)
        if "alias" in kwargs:
            self.alias = kwargs["alias"]
        else:
            self.alias = None
        for node in argnodes:
            self._instrument(frame, node)

    def _instrument(self, frame, node):
        code = compile(ast_transform(node), "<string>", "exec")
        frame.f_locals["_watch_transform"] = self.transform
        exec(code, {}, frame.f_locals)
        frame.f_locals.pop("_watch_transform")

    def transform(self, val):
        if type(val) is list:
            return WatchList(val, alias=self.alias)
