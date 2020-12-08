# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import sys
import pprint


class WatchPrint:
    def __init__(self, file=sys.stderr):
        self.file = file

    def __call__(self, frame, elem, exec_info):
        if elem.printer:
            p = elem.printer
        else:
            p = self.printer
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
        return f"{exec_info[0]} ({exec_info[1]}:{exec_info[2]}):"

    def printer(self, obj):
        if type(obj) is str:
            print(obj, file=self.file)
        else:
            pprint.pprint(obj, stream=self.file)
