#!/usr/bin/env python3

import ast
import os

def getAllPythonFiles(path):
    folders = [path]

    while folders:
        folder = folders.pop()
        for entry in os.scandir(folder):
            if entry.is_dir():
                folders.append(entry.path)
            elif entry.is_file() and entry.path[-2:] == 'py':
                yield entry.path

loc = '/Users/thang/work/paperspace/repos/numpy'

def getAST(filePath):
    with open(filePath) as f:
        return ast.parse(f.read())

# via: https://docs.python.org/3/library/ast.html#ast.NodeVisitor
class ImportNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = set()

    def visit_Import(self, node):
        for ast_alias in node.names:
            self.imports.add(ast_alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for ast_alias in node.names:
            self.imports.add("{}.{}".format(node.module, ast_alias.name))
        self.generic_visit(node)

    def getImports(self):
        return self.imports

def main():
    f = '/Users/thang/work/paperspace/repos/numpy/runtests.py'
    tree = getAST(f)

    visitor = ImportNodeVisitor()
    visitor.visit(tree)
    x = visitor.getImports()
    print(x)

if __name__ == '__main__':
    main()
