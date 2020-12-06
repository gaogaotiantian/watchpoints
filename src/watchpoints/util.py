# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import ast
from io import StringIO
import sys
from tokenize import generate_tokens, NEWLINE, INDENT, NL


def getline(frame):
    """
    get the current logic line from the frame
    """
    lineno = frame.f_lineno
    filename = frame.f_code.co_filename

    with open(filename, "r") as f:
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
            elif toknum != INDENT and toknum != NL:
                lst.append(tokval)

    return code_string


def getargnodes(frame):
    """
    get the list of arguments of the current line function
    """
    line = getline(frame)
    try:
        tree = ast.parse(line)
        return tree.body[0].value.args
    except Exception:
        raise Exception("Unable to parse the line {}".format(line))
