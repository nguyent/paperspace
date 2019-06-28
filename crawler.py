#!/usr/bin/env python3

import argparse
import ast
import os
from pprint import pprint

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
        return sorted(list(self.imports), key = lambda x: x.lower())

class ProjectAnalyzer:
    def __init__(self, projectPath):
        self.path = projectPath
        self.imports = {}

    def getAST(filePath):
        with open(filePath, 'r') as f:
            return ast.parse(f.read())

    def getAllPythonFiles(self):
        folders = [self.path]

        while folders:
            folder = folders.pop()
            for entry in os.scandir(folder):
                if entry.is_dir():
                    folders.append(entry.path)
                elif entry.is_file() and entry.path[-3:] == '.py':
                    yield entry.path

    def processFile(self, filePath):
        tree = ProjectAnalyzer.getAST(filePath)
        visitor = ImportNodeVisitor()
        visitor.visit(tree)
        self.imports[filePath] = visitor.getImports()

    def analyze(self):
        for filePath in self.getAllPythonFiles():
            self.processFile(filePath)

    def getImports(self):
        return self.imports

def validatePath(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError("Path must be an existing directory")
    return path

def parseArguments():
    parser = argparse.ArgumentParser(description='Find all python files and their imports in a given directory')
    parser.add_argument('project_path', type=validatePath)
    return parser.parse_args().project_path

def main():
    projectPath = parseArguments()
    analyzer = ProjectAnalyzer(projectPath)
    analyzer.analyze()
    pprint(analyzer.getImports())

if __name__ == '__main__':
    main()
