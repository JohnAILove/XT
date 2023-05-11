# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/18 23:40
@Auth ： 大雄
@File ：processControl.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import time

from Unit.taskControl import *
from Common.publicFunction import *
from public import *

def processControl(row_num):
    package_name = get_script_value(gl_info.script,"package_name")
    td_info[row_num].package_name = package_name
    td_info[row_num].progress = "等待模拟器桌面显示"
    td_info[row_num].desktop_delay_num = desktop_delay_num # 初始化模拟器启动等待时间
    td_info[row_num].start_app_delay = start_app_delay # 初始化app启动等待时间
    td_info[row_num].restart_app_num = restart_num
    max_time = process_max_time+time.time()
    pro_dict = {
        "等待模拟器桌面显示":(delay_desktop,(row_num,)),
        "启动app": (runApp, (row_num, package_name)),
        "重启app": (restartApp, (row_num, package_name)),
        "游戏操作": (gameControl, (row_num,)),
        "停止": ["任务完成", "模拟器启动卡死","启动app卡死","启动游戏卡死","任务异常", "·", "未安装游戏", "app卡死","手动停止","已超14天","主线任务超时"],
        "重启模拟器":(restart_ld,(row_num,package_name))
    }
    while True:
        time.sleep(2)
        if max_time < time.time():
            update_log("流程超时,为避免开始",row_num)
            update_task(row_num,f"流程超时{process_max_time/60}分钟")
            return

        for k,v in pro_dict.items():
            progress = td_info[row_num].progress
            if progress in pro_dict["停止"]:
                update_log(f"流程控制：{progress}", row_num)
                update_task(row_num, progress)
                if progress == "模拟器启动卡死":
                    td_info[row_num].progress = "重启模拟器"
                    break
                gl_info.csv.edit_cell(row_num+1,6,str(progress))
                return
            elif k==progress:
                update_log(f"流程控制：{progress}", row_num)
                update_task(row_num, progress)
                v[0](*v[1])
                update_task(row_num,k)
                break
        else:
            update_log(f"流程控制没有该流程 {progress}",row_num)
            update_task(row_num,"流程异常")
            raise "流程异常"
