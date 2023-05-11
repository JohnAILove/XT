# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/19 0:20
@Auth ： 大雄
@File ：taskControl.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import time

from Common.getAppName import get_ld_app_name
from Unit.task import *

# 模拟器启动后,等待桌面显示
def delay_desktop(row_num):
    # 初始化时间
    max_time = time.time() + desktop_delay_num
    # 判断模拟器是否显示桌面超时
    while True:
        if max_time<time.time():
            update_log("等待模拟器超时",row_num)
            break
        time.sleep(5)
        update_log(f"等待桌面显示...{int(max_time-time.time())}s",row_num)
        ldNum = gl_info.all_ld[row_num].index
        update_log("获取顶层界面app名称",row_num)
        app_name = get_ld_app_name(ldNum)
        update_log(f"当前名称{app_name}",row_num)
        if app_name == desktop_name:
            td_info[row_num].progress = "启动app"
            return True
    td_info[row_num].progress = "模拟器启动卡死"
    return False

# 启动app
def runApp(row_num,package_Name):
    update_log("启动app",row_num)
    ldNum = gl_info.all_ld[row_num].index
    time.sleep(1)
    ld = gl_info.ld
    update_log("判断app是否安装",row_num)
    if ld.has_install(ldNum,package_Name):
        if package_Name not in ld.get_activity_name(ldNum):
            update_log("app已安装未启动,准备启动app", row_num)
            ld.invokeapp(ldNum, package_Name)
            td_info[row_num].progress = "游戏操作"
        else:
            update_log("app已启动", row_num)
            td_info[row_num].progress = "游戏操作"
        return True
    else:
        td_info[row_num].progress = "未安装游戏"
        return False
    # td_info[row_num].progress = "启动app卡死"
    # return False


# 游戏操作
def gameControl(row_num):
    update_log("启动游戏主任务",row_num)
    task_class_name = get_script_value(gl_info.script,"task_class_name")
    flag = eval(task_class_name)(row_num).task()
    td_info[row_num].progress = flag

# 重启模拟器
def restart_ld(row_num,package_name):
    if td_info[row_num].restart_num >0:
        td_info[row_num].restart_num -=1
        update_log(f"第{restart_num-td_info[row_num].restart_num}次重启模拟器并打开app,等待{desktop_delay_num+start_app_delay}s",row_num)
        ldNum = gl_info.all_ld[row_num].index
        gl_info.ld.restart(ldNum,package_name) # 重启并打开app
        for i in range(desktop_delay_num+start_app_delay):
            update_log(f"重启等待倒数 {desktop_delay_num+start_app_delay-i}s",row_num)
            time.sleep(1)
            if gl_info.all_ld[row_num].is_in_android:
                break
        td_info[row_num].desktop_delay_num == desktop_delay_num
        td_info[row_num].progress = "游戏操作"
    else:
        update_log("已重启三次模拟器,不在重启",row_num)
        td_info[row_num].progress = "异常停止"

# 重启app
def restartApp(row_num,package_name):
    # 保存截图

    # 检测图像保存路径是否正常
    gl_info.ld.set_sharedPictures(gl_info.all_ld[row_num].index, path)
    # 重启超过3次则任务异常
    if td_info[row_num].restart_app_num > 0:
        td_info[row_num].restart_app_num -= 1
        update_log(f"第{restart_num - td_info[row_num].restart_app_num}次 重启app,并等待{start_app_delay}",row_num)
        td_info[row_num].gp.restart_app(package_name)
        for i in range(start_app_delay):
            update_log(f"重启等待倒数 {start_app_delay - i}s")
            time.sleep(1)
            if gl_info.all_ld[row_num].is_in_android:
                break

        update_log("已重启app",row_num)
        td_info[row_num].progress = "游戏操作"
    else:
        td_info[row_num].progress = "启动app卡死"