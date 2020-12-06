# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import ast
from tokenize import generate_tokens, NEWLINE, INDENT, NL
from io import StringIO


def getline(frame):
    """
    get the current logic line from the frame
    """
    lineno = frame.f_lineno
    filename = frame.f_code.co_filename

    with open(filename, "r") as f:
        linesio = StringIO("".join(f.readlines()[lineno - 1:]))
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
