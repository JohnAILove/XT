# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/18 16:22
@Auth ： 大雄
@File ：model.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import threading


class Custom:
    def __init__(self):
        self.processP = None # 进程
        self.thread = None
        self.hwnd = None
        self.title = None
        self.user = None
        self.password = None
        self.server = None
        self.task = None
        self.progress = None
        self.point = None
        self.thread_is_alive = None
        self.Event:threading.Event = None
        self.row_nums = []
        self.index = None # 雷电序号
        self.ld = None # 雷电对象
        self.ld_t= None # 雷电线程
        self.ld_stop_t = None # 雷电停止线程
        self.ld_list_t = None # 更新雷电数据的线程
        self.all_ld_t = None # 雷电线程 用于启动所有模拟器
        self.ldNum = None  # 雷电序号
        self.out_ldNum = None # 排除雷电模拟器序号
        self.all_ld = None # 雷电所有序号列表信息
        self.mainView = None
        self.queue_num = 0
        self.script = None # 脚本
        self.gp = None  # 游戏插件
        self.ld_path = None # 雷电参数
        self.init_ld = None # 初始化模拟器线程
        self.bubing = None # 补兵流程
        self.meiri = None # 每日副本流程

    def clear(self):
        self.__init__()

def tdi():
    re = []
    for i in range(1000):
        re.append(Custom())
    return re

gl_info = Custom()
td_info = tdi()