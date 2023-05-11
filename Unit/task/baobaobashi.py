# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/19 18:52
@Auth ： 大雄
@File ：baobaobashi.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import time
from Common.publicFunction import update_log, get_script_value
from public import *


class BaoBaoBaShi_task:
    def __init__(self,row_num):
        self.row_num = row_num
        self.ldNum = gl_info.all_ld[row_num].index
        self.ms = gl_info.ms
        self.gp = td_info[row_num].gp

    def task(self):
        while True:
            time.sleep(1)
            progress = td_info[self.row_num].progress

            if progress == "游戏操作":
                self.gameEnter()

            elif progress == "游戏登录":
                self.gameLogin()

            elif progress == "主线任务":
                td_info[self.row_num].progress = self.task_mian()

            else:break

        return td_info[self.row_num].progress

    def task_mian(self):
        dic = self.ms["任务"]
        for k,tz in dic.items():
            if self.game_run(tz):
                if "2" in k:
                    if not self.back():return "任务异常"
            else:
                return "任务异常"
        return "任务完成"

    # 游戏进入
    def gameEnter(self):
        for i in range(60):
            time.sleep(1)
            update_log(f"等待app启动到游戏主界面",self.row_num)
            max_loc = self.gp.find_pic(*self.ms["游戏主界面"])
            if max_loc:
                self.gp.left_click(*max_loc)
                update_log("点击游戏主界面",self.row_num)
                td_info[self.row_num].progress = "游戏登录"
                return
        td_info[self.row_num].progress = "app卡死"

    # 游戏登录
    def gameLogin(self):
        td_info[self.row_num].progress = "主线任务"


    # 找图并点击
    def game_run(self,tz):
        for i in range(10):
            time.sleep(1)
            max_loc = self.gp.find_pic(*tz)
            if max_loc:
                update_log(f"点击 {max_loc}",self.row_num)
                self.gp.left_click(*max_loc)
                return True

    # 后退
    def back(self):
        update_log(f"后退",self.row_num)
        return self.game_run(self.ms["back"])



