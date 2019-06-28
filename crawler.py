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

f = '/Users/thang/work/paperspace/repos/numpy/runtests.py'

# An abs file path
def getAST(filePath):
    with open(filePath) as f:
        return ast.parse(f.read())

print(getAST(f))
