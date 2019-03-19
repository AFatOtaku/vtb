# coding=utf-8
import os


# 获得文件中的LIST列表
def readlist(name):
    path = os.path.dirname(os.path.realpath(__file__));
    file = open(path + '\\listTxt\\' + name, 'r')
    lines = file.read().splitlines()
    file.close()
    return lines


# 清空文档
def cleanlist(name):
    path = os.path.dirname(os.path.realpath(__file__));
    file = open(path + '\\listTxt\\' + name, "r+", encoding="utf-8")
    file.seek(36)
    file.truncate()
    file.close()


# 向文档中写入LIST
def writelist(name, list):
    path = os.path.dirname(os.path.realpath(__file__));
    file = open(path + '\\listTxt\\' + name, "r+", encoding="utf-8")
    for item in list:
        file.write(str(item) + '\n')
    file.close()
