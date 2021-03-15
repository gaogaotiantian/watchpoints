# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from bdb import BdbQuit
import inspect
import pdb
import sys
import threading
from .util import getargnodes
from .watch_element import WatchElement
from .watch_print import WatchPrint


class Watch:
    def __init__(self):
        self.watch_list = []
        self.tracefunc_stack = []
        self.enable = False
        self.stack_limit = 5
        self.set_lock = threading.Lock()
        self.tracefunc_lock = threading.Lock()
        self.restore()

    def __call__(self, *args, **kwargs):
        with self.set_lock:
            frame = inspect.currentframe().f_back
            argnodes = getargnodes(frame)
            for node, name in argnodes:
                self.watch_list.append(
                    WatchElement(
                        frame,
                        node,
                        alias=kwargs.get("alias", None),
                        default_alias=name,
                        callback=kwargs.get("callback", None),
                        track=kwargs.get("track", ["variable", "object"]),
                        when=kwargs.get("when", None),
                        deepcopy=kwargs.get("deepcopy", False),
                        cmp=kwargs.get("cmp", None),
                        copy=kwargs.get("copy", None),
                        watch_print=WatchPrint(
                            file=kwargs.get("file", self.file),
                            stack_limit=kwargs.get("stack_limit", self.stack_limit)
                        )
                    )
                )

            if not self.enable and self.watch_list:
                self.start_trace(frame)

            del frame

    def start_trace(self, frame):
        if not self.enable:
            self.enable = True
            self.tracefunc_stack.append(sys.gettrace())
            self._prev_funcname = frame.f_code.co_name
            self._prev_filename = frame.f_code.co_filename
            self._prev_lineno = frame.f_lineno
            while frame:
                frame.f_trace = self.tracefunc
                frame = frame.f_back

            sys.settrace(self.tracefunc)
            threading.settrace(self.tracefunc)

    def stop_trace(self, frame):
        if self.enable:
            self.enable = False
            tf = self.tracefunc_stack.pop()
            frame.f_trace = tf
            while frame:
                frame.f_trace = tf
                frame = frame.f_back

            sys.settrace(tf)
            threading.settrace(tf)

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

        if "pdb" in kwargs:
            self.pdb = pdb.Pdb()
            self.pdb.reset()

        if "file" in kwargs:
            self.file = kwargs["file"]

        if "stack_limit" in kwargs:
            self.stack_limit = kwargs["stack_limit"]

    def restore(self):
        self._callback = self._default_callback
        self.pdb = None
        self.file = sys.stderr
        self.pdb_enable = False

    def install(self, func="watch"):
        import builtins
        setattr(builtins, func, self)

    def uninstall(self, func="watch"):
        import builtins
        if hasattr(builtins, func):
            delattr(builtins, func)

    def tracefunc(self, frame, event, arg):
        with self.tracefunc_lock:
            dirty = False
            for elem in self.watch_list:
                changed, exist = elem.changed(frame)
                if changed:
                    if not elem.when or elem.when(elem.obj):
                        if self.pdb:
                            self.pdb_enable = True
                        if elem._callback:
                            elem._callback(frame, elem, (self._prev_funcname, self._prev_filename, self._prev_lineno))
                        else:
                            self._callback(frame, elem, (self._prev_funcname, self._prev_filename, self._prev_lineno))
                    elem.update()
                if not exist:
                    elem.exist = False
                    dirty = True
            if dirty:
                self.watch_list = [elem for elem in self.watch_list if elem.exist]

            self._prev_funcname = frame.f_code.co_name
            self._prev_filename = frame.f_code.co_filename
            self._prev_lineno = frame.f_lineno

            if self.pdb_enable:
                try:
                    self.pdb.trace_dispatch(frame, event, arg)
                except BdbQuit:
                    self.pdb_enable = False
                    self.pdb.reset()
                    # BdbQuit will clear sys.settrace()
                    # We need to get it back
                    sys.settrace(self.tracefunc)

        return self.tracefunc

    def _default_callback(self, frame, elem, exec_info):
        elem.watch_print(frame, elem, exec_info)
