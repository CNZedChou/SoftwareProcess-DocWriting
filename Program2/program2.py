# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Zed
@Version        :  V1.0.0
------------------------------------
@File           :  program2.py
@Description    :  
@CreateTime     :  2020-10-15 20:23
------------------------------------
@ModifyTime     :  
"""
import os
import ast


def count_all(code):
    scriptLine = 0
    countLine = 0
    flag = True
    for line in code.readlines():
        #         # 空行不统计
        line = line.strip()
        if not len(line):
            continue
        # 注意下面的这两个elif必须要前面，这样子当('"""')结束之后及时将flag置为True
        if line.endswith('"""') and flag == False:
            flag = True
            continue
        if line.endswith("'''") and flag == False:
            flag = True
            continue
        if not flag:
            continue
        if line.startswith("# !") or line.startswith("# -*-") or line.startswith("# encoding"):
            scriptLine += 1
            countLine += 1
        # 如果以“#”号开头的，不统计
        elif line.startswith("#"):
            continue
        # 如果同时以("'''")或者('"""')开头或者结尾（比如："""aaa"""），那么不统计
        elif line.startswith('"""') and line.endswith('"""') and line != '"""':
            continue
        elif line.startswith("'''") and line.endswith("'''") and line != "'''":
            continue
        # 如果以("'''")或者('"""')开头或者结尾（比如：aaa"""或者"""bbb），那么不统计
        # 注意下面的这两个elif必须要放后面
        elif line.startswith('"""') and flag == True:
            flag = False
            continue
        elif line.startswith("'''") and flag == True:
            flag = False
            continue
        else:
            countLine += 1
    return countLine,scriptLine


class ClassCounter(ast.NodeVisitor):


    def __init__(self, filename):
        self.class_count = 0
        self.func_count = 0
        self.import_count = 0
        self.entry_point = 0
        self.expr_count = 0
        self.classLine = []
        self.funcLine = []
        self.importLine = []
        self.ifLine = []
        self.exprLine = []
        with open(filename,'r',encoding='utf-8') as f:
            module = ast.parse(f.read())
            self.visit(module)

    def visit_ClassDef(self, node):
        self.classLine.append(node.lineno)
        # print('class: {}'.format(node.lineno))
        self.class_count += 1

    def visit_FunctionDef(self,node):
        self.funcLine.append(node.lineno)
        # print('func: {}'.format(node.lineno))
        self.func_count += 1

    def visit_Import(self,node):
        self.importLine.append(node.lineno)
        # print('imports: {}'.format(node.lineno))
        self.import_count += 1

    def visit_If(self,node):
        self.ifLine.append(node.lineno)
        # print('If: {}'.format(node.lineno))
        self.entry_point += 1

    def visit_Expr(self,node):
        self.exprLine.append(node.lineno)
        self.expr_count += 1


class InClassFunctions(object):
    def __init__(self, node):
        self.classFuncCount = []
        self.node = node
        self.loc_in_class = 0
        self.classCount = []
    def get_attribute_names(self):
        for cls in self.node.body:
            # print(self.node.body)
            if isinstance(cls, ast.ClassDef):
                self.loc_in_method = 0
                self.loc_in_class += 1
                self.classCount.append(self.loc_in_class)
                for node in ast.walk(cls):
                    if isinstance(node, ast.FunctionDef):
                        self.loc_in_method += 1
                        # print('Method {}'.format(self.loc_in_method))
                self.classFuncCount.append(self.loc_in_method)
                # print('Class {} has {} functions'.format(self.loc_in_class,self.loc_in_method))


if __name__ == '__main__':
    filename = 'test.py'
    empty = 2
    code_file = open(filename, "r", encoding='utf-8')
    totalLine,scriptLine = count_all(code_file)
    originalLine = len(open(filename, "r", encoding='utf-8').readlines())
    print('Total lines of code:', totalLine)
    print('Original total lines:', originalLine)
    print('----------------------------------------------------------')
    classCounter = ClassCounter('test.py')
    # print('Number of Expr: {}'.format(classCounter.expr_count))
    # print('original line number of Expr part', classCounter.exprLine)
    # print('----------------------------------------------------------')
    print('Number of imports: {}'.format(classCounter.import_count))
    print('original line number of Import part',classCounter.importLine)
    print('----------------------------------------------------------')
    print('Number of classes: {}'.format(classCounter.class_count))
    print('original line number of class part',classCounter.classLine)
    print('----------------------------------------------------------')
    print('Number of Functions(Top-Level): {}'.format(classCounter.func_count))
    print('original line number of function part',classCounter.funcLine)
    print('----------------------------------------------------------')
    print('Number of entry_point: {}'.format(classCounter.entry_point))
    print('original line number of entry_point part',classCounter.ifLine)
    print('----------------------------------------------------------')
    incClassFunc = InClassFunctions(ast.parse(open(filename, "r", encoding='utf-8').read()))
    incClassFunc.get_attribute_names()
    # print(sum(incClassFunc.classFuncCount))
    print('Part Script declaration size:',scriptLine)
    print('Part Import size:',classCounter.classLine[0] - classCounter.importLine[0] - empty)
    print('Part Classes size:',classCounter.ifLine[0] - classCounter.classLine[0] - empty*(sum(incClassFunc.classFuncCount)))
    print('Part Functions(Top-Level) size:', sum(classCounter.funcLine))
    # print('Part Classes size:',
    #       classCounter.classLine[1] - classCounter.classLine[0] - empty*incClassFunc.classFuncCount[0] + classCounter.ifLine[0] - classCounter.classLine[1] - empty * incClassFunc.classFuncCount[1])
    # print('Part Functions size:',classCounter.classLine[0] - classCounter.importLine - empty)
    print('Part Entry-Point size:',originalLine - classCounter.ifLine[0] + 1)


