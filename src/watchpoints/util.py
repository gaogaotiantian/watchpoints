# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import ast
from io import StringIO
import inspect
import re
try:
    import readline
except ImportError:
    pass
import sys
from tokenize import generate_tokens, NEWLINE, COMMENT, INDENT, NL


def getline(frame):
    """
    get the current logic line from the frame
    """
    lineno = frame.f_lineno
    filename = frame.f_code.co_filename

    if filename == "<stdin>":
        try:
            his_length = readline.get_current_history_length()
            code_string = readline.get_history_item(his_length)
        except NameError:
            raise Exception("watchpoints does not support REPL on Windows")
    elif filename.startswith("<ipython-input"):
        return inspect.getsource(frame)
    else:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if sys.version_info.minor <= 7:
                # For python 3.6 and 3.7, f_lineno does not return correct position
                # when it's multiline code
                while "(" not in lines[lineno - 1]:
                    lineno -= 1
            linesio = StringIO("".join(lines[lineno - 1:]))
            lst = []
            code_string = ""
            for toknum, tokval, _, _, _ in generate_tokens(linesio.readline):
                if toknum == NEWLINE:
                    code_string = " ".join(lst)
                    break
                elif toknum not in (COMMENT, NL, INDENT):
                    lst.append(tokval)

    return code_string


def getargnodes(frame):
    """
    get the list of arguments of the current line function
    """
    line = getline(frame)
    m = re.match(r".*?\((.*)\)", line)
    if not m:  # pragma: no cover
        raise Exception(f"Unable to locate watch line {line}")
    args = ["".join(s.strip().split()) for s in m.group(1).split(",")]
    try:
        tree = ast.parse(line)
        return zip(tree.body[0].value.args, args[:len(tree.body[0].value.args)])
    except Exception:
        raise Exception(f"Unable to parse the line {line}")
