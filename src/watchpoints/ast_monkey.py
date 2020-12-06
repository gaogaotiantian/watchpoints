# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/watchpoints/blob/master/NOTICE.txt


import ast
import copy


def to_store(node):
    node.ctx = ast.Store()
    return node


def ast_transform(node):
    """
    :param ast.Node node: an ast node representing an expression of variable

    :return ast.Node: an ast node for ```var = transform(var)```
    """
    root = ast.Module(
        body=[
            ast.Assign(
                targets=[
                    to_store(copy.deepcopy(node))
                ],
                value=ast.Call(
                    func=ast.Name(id="_watch_transform", ctx=ast.Load()),
                    args=[
                        node
                    ],
                    keywords=[]
                )
            )
        ],
        type_ignores=[]
    )
    ast.fix_missing_locations(root)

    return root
