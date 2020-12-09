# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from .ast_monkey import ast_parse_node
import copy


class WatchElement:
    def __init__(self, frame, node, alias=None, default_alias=None, callback=None, track=["variable", "object"]):
        code = compile(ast_parse_node(node), "<string>", "exec")
        f_locals = frame.f_locals
        exec(code, {}, f_locals)
        self.frame = frame
        self.obj = f_locals.pop("_watchpoints_obj")
        self.prev_obj = self.obj
        self.localvar = None
        self.parent = None
        self.subscr = None
        self.attr = None
        for var in ("_watchpoints_localvar", "_watchpoints_parent", "_watchpoints_subscr", "_watchpoints_attr"):
            if var in f_locals:
                setattr(self, var.replace("_watchpoints_", ""), f_locals.pop(var))
        self.update()
        self.alias = alias
        self.default_alias = default_alias
        self._callback = callback
        self.exist = True
        self.track = track

    @property
    def track(self):
        return self._track

    @track.setter
    def track(self, val):
        if type(val) is list:
            for elem in val:
                if elem not in ("variable", "object"):
                    raise ValueError("track only takes list with 'variable' or 'object'")
            if len(val) == 0:
                raise ValueError("You need to track something!")
            self._track = val[:]
        elif type(val) is str:
            if val not in ("variable", "object"):
                raise ValueError("track only takes list with 'variable' or 'object'")
            self._track = [val]
        else:
            raise TypeError("track only takes list with 'variable' or 'object'")

    def changed(self, frame):
        """
        :return (changed, exist):
        """
        if "variable" in self.track:
            if frame is self.frame and self.localvar is not None:
                if self.localvar in frame.f_locals:
                    if frame.f_locals[self.localvar] != self.obj:
                        self.obj = frame.f_locals[self.localvar]
                        return True, True
                else:
                    return True, False

            if self.parent is not None and self.subscr is not None:
                try:
                    if self.parent[self.subscr] != self.obj:
                        self.obj = self.parent[self.subscr]
                        return True, True
                except (IndexError, KeyError):
                    return True, False
            elif self.parent is not None and self.attr is not None:
                try:
                    if getattr(self.parent, self.attr) != self.obj:
                        self.obj = getattr(self.parent, self.attr)
                        return True, True
                except AttributeError:
                    return True, False
        if "object" in self.track:
            return self.obj != self.prev_obj, True

        return False, True

    def update(self):
        self.prev_obj = copy.deepcopy(self.obj)

    def same(self, other):
        if type(other) is str:
            return self.alias and self.alias == other
        else:
            return other is self.obj

    def belong_to(self, lst):
        return any((self.same(other) for other in lst))
