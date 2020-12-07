# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from .ast_monkey import ast_parse_node
import copy


class WatchElement:
    def __init__(self, frame, node, alias=None, default_alias=None):
        code = compile(ast_parse_node(node), "<string>", "exec")
        f_locals = frame.f_locals
        exec(code, {}, f_locals)
        self.frame = frame
        self.obj = f_locals.pop("_watchpoints_obj")
        self.localvar = None
        self.parent = None
        self.subscr = None
        for var in ("_watchpoints_localvar", "_watchpoints_parent", "_watchpoints_subscr"):
            if var in f_locals:
                setattr(self, var.replace("_watchpoints_", ""), f_locals.pop(var))
        self.update()
        self.alias = alias
        self.default_alias = default_alias

    def changed(self, frame):
        if frame is self.frame:
            if self.localvar in frame.f_locals:
                if frame.f_locals[self.localvar] != self.obj:
                    self.prev_obj = self.obj
                    self.obj = frame.f_locals[self.localvar]
                    return True
        if self.parent and self.subscr:
            if self.parent[self.subscr] != self.obj:
                self.prev_obj = self.obj
                self.obj = self.parent[self.subscr]
                return True
        return self.obj != self.prev_obj

    def update(self):
        self.prev_obj = copy.deepcopy(self.obj)

    def same(self, other):
        if type(other) is str:
            return self.alias and self.alias == other
        else:
            return other is self.obj

    def belong_to(self, lst):
        return any((self.same(other) for other in lst))
