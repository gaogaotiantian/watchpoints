# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import sys


class WatchPrint:
    def __init__(self, file=sys.stderr):
        self.file = file

    def __call__(self, frame, elem, exec_info):
        self.p(self._file_string(exec_info))
        self.p(elem.prev_obj)
        self.p("->")
        self.p(elem.obj)
        self.p()

    def _file_string(self, exec_info):
        return f"{exec_info[0]} ({exec_info[1]}:{exec_info[2]}):"

    def p(self, *objects):
        print(*objects, sep=' ', end='\n', file=self.file, flush=False)
