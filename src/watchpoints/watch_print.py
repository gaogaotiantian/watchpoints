# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import sys


class WatchPrint:
    def __init__(self, print_type, file=sys.stderr):
        self.print_type = print_type
        self.file = file

    def __call__(self, frame, method, local_vars, when):
        if self.print_type == "list":
            self._print_list(frame, method, local_vars, when)

    def _file_string(self, frame):
        return f"{frame.f_code.co_name} ({frame.f_code.co_filename}:{frame.f_lineno}):"

    def _print_list(self, frame, method, local_vars, when):
        if when == "pre":
            self.p(self._file_string(frame))
            if local_vars['self']._alias:
                self.p(f"{local_vars['self']._alias} = {local_vars['self']}")
            else:
                self.p(f"{local_vars['self']}")

            method_name = method.__name__
            args = local_vars['args']
            if method_name == "__setitem__":
                self.p(f"setitem [{args[0]}] = {args[1]}")
            elif method_name == "append":
                self.p(f"append({args[0]})")
            elif method_name == "extend":
                self.p(f"extend({args[0]})")
            elif method_name == "insert":
                self.p(f"insert({args[0]}, {args[1]})")
            elif method_name == "remove":
                self.p(f"remove({args[0]})")
            elif method_name == "pop":
                if args:
                    self.p(f"pop({args[0]})")
                else:
                    self.p("pop()")
            elif method_name == "clear":
                self.p("clear()")
            elif method_name == "sort":
                self.p("sort()")
            elif method_name == "reverse":
                self.p("reverse()")

        elif when == "post":
            self.p(f"->{local_vars['self']}")
            self.p("")

    def p(self, *objects):
        print(*objects, sep=' ', end='\n', file=self.file, flush=False)
