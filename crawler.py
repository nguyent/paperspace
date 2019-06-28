#!/usr/bin/env python3

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
print(getAllPythonFiles(loc))
