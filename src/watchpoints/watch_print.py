# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import sys
import pprint
import threading


class WatchPrint:
    def __init__(self, file=sys.stderr):
        self.file = file

    def __call__(self, frame, elem, exec_info):
        p = self.printer
        if threading.active_count() > 1:
            curr_thread = threading.current_thread()
            p(f"> {curr_thread.name}")
        p(self._file_string(exec_info))
        p(f"> {self.getsourceline(exec_info)}")
        if elem.alias:
            p(f"{elem.alias}:")
        elif elem.default_alias:
            p(f"{elem.default_alias}:")
        p(elem.prev_obj)
        p("->")
        p(elem.obj)
        p("")

    def _file_string(self, exec_info):
        return f"> {exec_info[0]} ({exec_info[1]}:{exec_info[2]}):"

    def getsourceline(self, exec_info):
        try:
            with open(exec_info[1]) as f:
                lines = f.readlines()
                return f"    {lines[exec_info[2] - 1].strip()}"
        except (FileNotFoundError, PermissionError):
            return "unable to locate the source"

    def printer(self, obj):
        if type(obj) is str:
            print(obj, file=self.file)
        else:
            pprint.pprint(obj, stream=self.file)
