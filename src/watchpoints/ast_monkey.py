# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import ast


def to_store(node):
    node.ctx = ast.Store()
    return node


def ast_parse_node(node):
    """
    :param ast.Node node: an ast node representing an expression of variable

    :return ast.Node: an ast node for ```_obj = var```
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

    ast.fix_missing_locations(root)

    return root
