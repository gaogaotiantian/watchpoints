# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import sys
import threading
from objprint import objstr
import os.path
import zipfile


class WatchPrint:
    def __init__(self, file=sys.stderr, stack_limit=None):
        self.file = file
        self.stack_limit = stack_limit

    def __call__(self, frame, elem, exec_info):
        p = self.printer
        p("====== Watchpoints Triggered ======")
        if threading.active_count() > 1:
            curr_thread = threading.current_thread()
            p(f"---- {curr_thread.name} ----")
        p("Call Stack (most recent call last):")

        curr_frame = frame.f_back
        frame_counter = 0
        trace_back_data = []
        while curr_frame and (self.stack_limit is None or frame_counter < self.stack_limit - 1):
            trace_back_data.append(self._frame_string(curr_frame))
            curr_frame = curr_frame.f_back
            frame_counter += 1

        for s in trace_back_data[::-1]:
            p(s)

        p(self._file_string(exec_info))
        if elem.alias:
            p(f"{elem.alias}:")
        elif elem.default_alias:
            p(f"{elem.default_alias}:")
        p(elem.prev_obj)
        p("->")
        p(elem.obj)
        p("")

    def _file_string(self, exec_info):
        return f"  {exec_info[0]} ({exec_info[1]}:{exec_info[2]}):\n" + \
            self.getsourceline(exec_info)

    def _frame_string(self, frame):
        return self._file_string((frame.f_code.co_name, frame.f_code.co_filename, frame.f_lineno))

    def getsourceline(self, exec_info):
        try:
            filename = exec_info[1]
            if os.path.exists(filename):
                with open(exec_info[1], encoding="utf-8") as f:
                    lines = f.readlines()
                    return f">   {lines[exec_info[2] - 1].strip()}"
            else:
                # We may have an egg file, we try to figure out if we have a zipfile
                # in the path and unzip that
                potential_egg = filename
                f_paths = []
                while os.path.dirname(potential_egg) != potential_egg:
                    potential_egg, f_path = os.path.split(potential_egg)
                    f_paths.append(f_path)
                    if zipfile.is_zipfile(potential_egg):
                        with zipfile.ZipFile(potential_egg) as zf:
                            with zf.open("/".join(reversed(f_paths))) as f:
                                lines = f.readlines()
                                return f">   {lines[exec_info[2] - 1].decode('utf-8').strip()}"
            return "unable to locate the source"
        except (FileNotFoundError, PermissionError):  # pragma: no cover
            return "unable to locate the source"

    def printer(self, obj):

        def do_print(obj, stream):
            if type(obj) is str:
                print(obj, file=stream)
            else:
                print(objstr(obj), file=stream)

        if isinstance(self.file, str):
            with open(self.file, "a") as f:
                do_print(obj, f)
        else:
            do_print(obj, self.file)
