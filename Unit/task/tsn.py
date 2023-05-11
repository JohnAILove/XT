# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/29 20:40
@Auth ： 大雄
@File ：tsn.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
from Common.publicFunction import *
from public import *
import random
from Unit.task.son_tsn import *

class Tsn_task(MeiRi,BuBing):
    def __init__(self, row_num):
        self.row_num = row_num
        self.ldNum = gl_info.all_ld[row_num].index
        self.ms = gl_info.ms
        self.gp = td_info[row_num].gp
        self.loc = gl_info.loc

        self.login_gift_max_num = 15  # 登录好礼最大天数
        self.resources_path = get_script_value(gl_info.script, "resources_path")
        self.package_name = get_script_value(gl_info.script, "package_name")

        self.restart_app_num = restart_num  # 重启app次数

        gl_info.csv.set_key(0)
        self.login_now_day = int(self.get_csv_column(1))  # 登入好礼当前领取天数
        self.lgoin_14_flag = False if "False" in self.get_csv_column(2) else True  # 登入好禮>=14天
        self.token = int(self.get_csv_column(3))  # 当前已有吞食币数量
        self.up_token = int(self.get_csv_column(4))  # 已上传市集的吞食币数量
        self.residue_token = int(self.get_csv_column(5))  # 剩余吞食币

        self.max_token = gl_info.tsn_token  # 提交的最大吞食币数量

        self.welfare_flag = None  # 福利领取状态
        self.login_flag = None  # 登入公告状态
        self.xinjian_flag = None
        self.start_app_delay = start_app_delay
        self.app_delay_num = app_delay_num
        self.dianxiaoer_time = get_script_value(gl_info.script, "dianxiaoer_time")
        self.task_max_time = get_script_value(gl_info.script, "task_max_time")
        self.bubing_task_time = get_script_value(gl_info.script, "bubing_task_time")
        self.paiqian_task_max_time = get_script_value(gl_info.script, "paiqian_task_max_time")
        self.update_delay = get_script_value(gl_info.script, "update_delay")
        self.bubing_zhuxian_flag = False  # 补兵任务是否到简佣家
        self.bubing_task_flag = False  # 补兵任务是否完成,包含武将是否已存入
    # 任务入口
    def task(self):
        if gl_info.fuli_state:
            return self.task_fuben()  # 福利和每日公用函数，内部在进行判断
        elif gl_info.bubing:
            return self.bubing()
        elif gl_info.meiri:
            return self.task_fuben()
