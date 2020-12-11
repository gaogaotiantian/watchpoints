# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import ast
import sys


def ast_parse_node(node):
    """
    :param ast.Node node: an ast node representing an expression of variable

    :return ast.Node: an ast node for:
        _watchpoints_obj = var
        if <var is a local variable>:
            # watch(a)
            _watchpoints_localvar = "a"
        elif <var is a subscript>:
            # watch(a[3])
            _watchpoints_parent = a
            _watchpoints_subscr = 3
        elif <var is an attribute>:
            # watch(a.b)
            _watchpoints_parent = a
            _watchpoints_attr = "b"
    """
    root = ast.Module(
        body=[
            ast.Assign(
                targets=[
                    ast.Name(id="_watchpoints_obj", ctx=ast.Store())
                ],
                value=node
            )
        ],
        type_ignores=[]
    )

    if type(node) is ast.Name:
        root.body.append(
            ast.Assign(
                targets=[
                    ast.Name(id="_watchpoints_localvar", ctx=ast.Store())
                ],
                value=ast.Constant(value=node.id)
            )
        )
    elif type(node) is ast.Subscript:
        root.body.append(
            ast.Assign(
                targets=[
                    ast.Name(id="_watchpoints_parent", ctx=ast.Store())
                ],
                value=node.value
            )
        )
        if sys.version_info.minor <= 8 and type(node.slice) is ast.Index:
            value_node = node.slice.value
        elif sys.version_info.minor >= 9 and type(node.slice) is not ast.Slice:
            value_node = node.slice
        else:
            raise ValueError("Slice is not supported!")

        root.body.append(
            ast.Assign(
                targets=[
                    ast.Name(id="_watchpoints_subscr", ctx=ast.Store())
                ],
                value=value_node
            )
        )
    elif type(node) is ast.Attribute:
        root.body.append(
            ast.Assign(
                targets=[
                    ast.Name(id="_watchpoints_parent", ctx=ast.Store())
                ],
                value=node.value
            )
        )
        root.body.append(
            ast.Assign(
                targets=[
                    ast.Name(id="_watchpoints_attr", ctx=ast.Store())
                ],
                value=ast.Constant(value=node.attr)
            )
        )

    ast.fix_missing_locations(root)

    return root
