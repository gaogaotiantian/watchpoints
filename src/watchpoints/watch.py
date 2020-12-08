# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import inspect
import sys
from .util import getargnodes
from .watch_element import WatchElement
from .watch_print import WatchPrint


class Watch:
    def __init__(self):
        self.watch_list = []
        self.tracefunc_stack = []
        self.enable = False
        self._callback = self._default_callback

    def __call__(self, *args, **kwargs):
        frame = inspect.currentframe().f_back
        argnodes = getargnodes(frame)
        for node, name in argnodes:
            self.watch_list.append(
                WatchElement(
                    frame,
                    node,
                    alias=kwargs.get("alias", None),
                    default_alias=name,
                    printer=kwargs.get("printer", None),
                    callback=kwargs.get("callback", None)
                )
            )

        if not self.enable and self.watch_list:
            self.start_trace(frame)

        del frame

    def start_trace(self, frame):
        if not self.enable:
            self.enable = True
            self.tracefunc_stack.append(sys.gettrace())
            sys.settrace(self.tracefunc)
            frame.f_trace = self.tracefunc
            self._prev_funcname = frame.f_code.co_name
            self._prev_filename = frame.f_code.co_filename
            self._prev_lineno = frame.f_lineno

    def stop_trace(self, frame):
        if self.enable:
            tf = self.tracefunc_stack.pop()
            sys.settrace(tf)
            frame.f_trace = tf
            self.enable = False

    def unwatch(self, *args):
        frame = inspect.currentframe().f_back
        if not args:
            self.watch_list = []
        else:
            self.watch_list = [elem for elem in self.watch_list if not elem.belong_to(args)]

        if not self.watch_list:
            self.stop_trace(frame)

        del frame

    def config(self, **kwargs):
        if "callback" in kwargs:
            self._callback = kwargs["callback"]

    def restore(self):
        self._callback = self._default_callback

    def tracefunc(self, frame, event, arg):
        dirty = False
        for elem in self.watch_list:
            changed, exist = elem.changed(frame)
            if changed:
                if elem.callback:
                    elem._callback(frame, elem, (self._prev_funcname, self._prev_filename, self._prev_lineno))
                else:
                    self._callback(frame, elem, (self._prev_funcname, self._prev_filename, self._prev_lineno))
                elem.update()
            if not exist:
                dirty = True

        if dirty:
            self.watch_list = [elem for elem in self.watch_list if elem.exist]

        self._prev_funcname = frame.f_code.co_name
        self._prev_filename = frame.f_code.co_filename
        self._prev_lineno = frame.f_lineno

        return self.tracefunc

    def _default_callback(self, frame, elem, exec_info):
        wp = WatchPrint()
        wp(frame, elem, exec_info)
