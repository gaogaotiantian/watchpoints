# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


from .ast_monkey import ast_parse_node
import copy


class WatchElement:
    def __init__(self, frame, node, **kwargs):
        code = compile(ast_parse_node(node), "<string>", "exec")
        f_locals = frame.f_locals
        exec(code, {}, f_locals)
        self.frame = frame
        self.obj = f_locals.pop("_watchpoints_obj")
        self.prev_obj = self.obj
        self.prev_obj_repr = self.obj.__repr__()
        self.localvar = None
        self.parent = None
        self.subscr = None
        self.attr = None
        for var in ("_watchpoints_localvar", "_watchpoints_parent", "_watchpoints_subscr", "_watchpoints_attr"):
            if var in f_locals:
                setattr(self, var.replace("_watchpoints_", ""), f_locals.pop(var))
        self.alias = kwargs.get("alias", None)
        self.default_alias = kwargs.get("default_alias", None)
        self._callback = kwargs.get("callback", None)
        self.exist = True
        self.track = kwargs.get("track", ["variable", "object"])
        self.when = kwargs.get("when", None)
        self.deepcopy = kwargs.get("deepcopy", False)
        self.cmp = kwargs.get("cmp", None)
        self.copy = kwargs.get("copy", None)
        self.update()

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
                    if frame.f_locals[self.localvar] is not self.obj:
                        self.obj = frame.f_locals[self.localvar]
                        return True, True
                else:
                    return True, False

            if self.parent is not None and self.subscr is not None:
                try:
                    if self.parent[self.subscr] is not self.obj:
                        self.obj = self.parent[self.subscr]
                        return True, True
                except (IndexError, KeyError):
                    return True, False
            elif self.parent is not None and self.attr is not None:
                try:
                    if getattr(self.parent, self.attr) is not self.obj:
                        self.obj = getattr(self.parent, self.attr)
                        return True, True
                except AttributeError:
                    return True, False
        if "object" in self.track:
            if not isinstance(self.obj, type(self.prev_obj)):
                raise Exception("object type should not change")  # pragma: no cover
            else:
                if self.cmp:
                    return self.cmp(self.prev_obj, self.obj), True
                elif self.obj.__class__.__module__ == "builtins":
                    return self.obj != self.prev_obj, True
                else:
                    guess = self.obj.__eq__(self.prev_obj)
                    if guess is NotImplemented:
                        if self.deepcopy:
                            raise NotImplementedError(
                                f"It's impossible to compare deepcopied customize objects. You need to define __eq__ method for {self.obj.__class__}")
                        return self.obj.__dict__ != self.prev_obj.__dict__, True
                    else:
                        return not guess, True

        return False, True

    def update(self):
        if self.copy:
            self.prev_obj = self.copy(self.obj)
        elif self.deepcopy:
            self.prev_obj = copy.deepcopy(self.obj)
        else:
            self.prev_obj = copy.copy(self.obj)
        self.prev_obj_repr = self.obj.__repr__()

    def same(self, other):
        if type(other) is str:
            return self.alias and self.alias == other
        else:
            return other is self.obj

    def belong_to(self, lst):
        return any((self.same(other) for other in lst))
