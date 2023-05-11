# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/28 20:01
@Auth ： 大雄
@File ：config_csv.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import csv
import os
import time


class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class CSV:
    def __init__(self, path):
        self.path = path
        if os.path.exists(self.path):
            with open(self.path, "r+", encoding="gbk") as fp:
                reader = csv.reader(fp)
                self.read_list = list(reader)
                self.max_line = len(self.read_list)
        else:
            with open(self.path, "w", encoding="gbk", newline='') as fp:
                self.read_list = []
                self.max_line = 0

    def open(self, flag, mode, func, args):
        if flag == "read":
            res = func(self.read_list, *args)
        elif flag == "write":
            with open(self.path, "w", encoding="gbk", newline='') as fp:
                write_obj = csv.writer(fp)
                res = func(mode, write_obj, *args)
        return res

    def __read(self, read_list, row=None):
        try:
            # 读取所有
            if row is None:
                res = read_list
            # 读取一行
            else:
                res = read_list[row]
        except:
            print("读取的行数内容不存在")
            res = None
        return res

    def __write(self, mode: str, write_obj, row: int, str_: list):
        if mode == "all" and type(str_[0]) == list:
            self.read_list = str_
            self.max_line = len(self.read_list)
        elif mode == "edit" and row < self.max_line:
            self.read_list[row] = str_
        elif mode == "add":
            self.read_list.append(str_)
            self.max_line += 1
        elif mode == "insert" and row <= self.max_line:
            self.read_list.insert(row,str_) # 超过则在最后一行插入
        elif mode == "del_line" and row < self.max_line:
            self.read_list.pop(row)
        else:
            write_obj.writerows(self.read_list) # 复原
            raise MyError(("参数有误",mode,write_obj,row,str_))
        write_obj.writerows(self.read_list)

    # 读取所有内容
    def read(self):
        return self.read_list

    # 读取某一行内容
    def read_line(self, row):
        return self.open("read", "line", self.__read, (row,))

    # 清空并写入所有内容
    def write(self, list_):
        self.open("write", "all", self.__write, (None, list_))

    # 指定行编辑内容
    def edit(self, row, list_):
        self.open("write", "edit", self.__write, (row, list_))

    def edit_cell(self,row,column,str_):
        list_ = self.read_line(row)
        list_[column] = str_
        self.edit(row,list_)

    # 添加一行内容
    def add(self, list_):
        return self.open("write", "add", self.__write, (self.max_line, list_,))

    # 插入一行
    def insert(self, row, list_):
        return self.open("write", "insert", self.__write, (row,list_))

    # 删除某一行
    def del_line(self,row):
        return self.open("write","del_line",self.__write,(row,None))

    # 设置某一列为下标
    def set_key(self, column):
        self.key_column = column

    # 获取下标key的行内容，或者行数
    def get_value(self, key,flag=None):
        for row,line in enumerate(self.read_list):
            if str(line[self.key_column]) == str(key):
                if not flag:
                    return line
                else:
                    return row
        print(f"无法找到下标{key}的行内容")

    # 对下标为key的所在行数，写入数据
    def set_key_value(self,key,list__):
        row = self.get_value(key,flag=True)
        self.edit(row,list__)

    # 获取某一列内容
    def get_column(self,column:int,first_line=None):
        column_list = []
        # 获取某一列内容
        for line in self.read_list:
            try:
                column_list.append(line[column])
            except:
                column_list.append("")
        return column_list

if __name__ == '__main__':
    # now_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    now_time = "2023-01-28-20-19-29"
    c = CSV(r"E:\code\python\xiaojia_Timo\2023-02-01_tsn.csv")
    c.set_key(0)
    print()