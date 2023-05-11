# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/27 23:38
@Auth ： 大雄
@File ：timo.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import random
import time

from Common.config_csv import CSV
from Common.publicFunction import update_log, get_script_value
from public import *

class Timo_task:
    def __init__(self,row_num):
        self.row_num = row_num
        self.ldNum = gl_info.all_ld[row_num].index
        self.ms = gl_info.ms
        self.gp = td_info[row_num].gp
        self.loc = gl_info.loc
        self.csv_path = project_path + "\\" + time.strftime('%Y-%m-%d', time.localtime(time.time())) + ".csv"
        self.input_flag_num = 500
        self.resources_path = get_script_value(gl_info.script,"resources_path")
    # 任务入口
    def task(self):
        while True:
            time.sleep(1)
            progress = td_info[self.row_num].progress
            update_log(progress,self.row_num)
            if progress == "游戏操作":
                self.gameEnter()

            elif progress == "游戏登录":
                self.gameLogin()

            elif progress == "主线任务":
                td_info[self.row_num].progress = self.task_main()

            else:break

        return progress

    # 游戏操作
    def gameEnter(self):
        for i in range(60):
            time.sleep(1)
            update_log(f"模拟器等待app启动到游戏主界面",self.row_num)
            if self.__find_pics_main():
                td_info[self.row_num].progress = "游戏登录"
                return
        td_info[self.row_num].progress = "app卡死"

    # 游戏登录
    def gameLogin(self):
        td_info[self.row_num].progress = "主线任务"

    # 主线任务
    def task_main(self):
        task_dict = {
            "点击 加号":(self.__find_pic_and_click, (self.ms["游戏主界面"], self.loc["加号"])),
            "点击 想法": (self.__find_pic_and_click, (self.ms["加号"], self.loc["想法"])),
            "点击 写些什么": (self.__find_pic_and_click, (self.ms["想法"], self.loc["写些什么"])),
            "输入数字":(self.__random_input_num,()),
            "点击 后退": (self.__back,()),
            # "查看文本":(self.__read_text,self.ms["查看文本"]),
            "点击 文本": (self.__find_pic_and_click, (self.ms["游戏主界面"], self.loc["点击文本"])),
            "点击 右上角": (self.__find_pic_and_click, (self.ms["右上角"], self.loc["右上角"])),
            "点击 删除": (self.__find_pic_and_click, (self.ms["删除"], self.loc["删除"])),
        }
        for k,v in task_dict.items():
            update_log(k,self.row_num)
            if not v[0](*v[1]):
                return "任务异常"
            time.sleep(1)
        return "任务完成"

    # 判断游戏是否已启动
    def __find_pics_main(self):
        pic_dict = {
            "游戏主界面":self.ms["游戏主界面"],
            "感谢使用Timo笔记": self.ms["感谢使用Timo笔记"],
        }
        for k,v in pic_dict.items():
            if self.gp.find_pic(*v):
                if k == "游戏主界面":
                    return True
                elif k == "感谢使用Timo笔记":
                    return self.__agree()

    # 同意并使用
    def __agree(self):
        for i in range(10):
            time.sleep(1)
            self.gp.slide(*self.loc["下拉"])
            max_loc= self.gp.find_pic(*self.ms["同意并使用"])
            if max_loc:
                # 下一页
                self.gp.left_click(*max_loc)
                for i in range(3):
                    time.sleep(1)
                    self.gp.left_click(*self.loc["下一页"])
                # 下拉选择默认主题
                for i in range(10):
                    self.gp.slide(*self.loc["下拉"])
                    max_loc =  self.gp.find_pic(*self.ms["创建已选主题并开始体验"])
                    if max_loc:
                        self.gp.left_click(*max_loc)
                        break
                return True

    # 随机输入数字
    def __random_input_num(self):
        input_num = random.randint(1, 1000)
        for i in range(10):
            time.sleep(1)
            if self.gp.find_pic(*self.ms["提示"]):
                self.gp.input(input_num)
                c = CSV(self.csv_path)
                flag = True if input_num >=self.input_flag_num else False
                c.add([self.ldNum,input_num,flag])
                return True

    # 找到图片,点击特定坐标
    def __find_pic_and_click(self,tz,loc):
        for i in range(10):
            time.sleep(1)
            if self.gp.find_pic(*tz):
                self.gp.left_click(*loc)
                return True

    # 后退
    def __back(self):
        self.gp.left_click(*self.loc["后退"])
        return True


