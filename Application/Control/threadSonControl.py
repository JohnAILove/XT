# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/15 16:11
@Auth ： 大雄
@File ：threadSonControl.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import threading
import time

from Application.model.model import td_info, gl_info
from Common.my_thread import MyThread
from Common.publicFunction import update_log, out_ldNumF


def resume_one_thread(row_num):
    # 查询对应 row_num 是否在启动过
    thread = td_info[row_num].thread
    if thread:
        # 启动过, 进行判断, 是否存活
        if thread.is_alive():
            # 显示界面
            update_log(row_num, "恢复线程", row_num)
            td_info[row_num].thread_status = "恢复线程"
            # 激活游戏,避免前台模式失败
            thread.resume()


def stop_one_thread(row_num):
    update_log("停止脚本", row_num)
    # 查询对应 row_num 是否在启动过
    t = td_info[row_num].thread
    if t and t.is_alive():
        # 显示界面
        update_log("停止线程", row_num)
        try:
            if td_info[row_num].thread:
                td_info[row_num].clear()
        except:
            update_log("清除线程数据失败，请勿反复清除", row_num)
        t.stop()


def update_ld_list():
    lock = threading.Lock()
    while True:
        temp = gl_info.ld.get_list(gl_info.out_ldNum)
        if temp:
            lock.acquire(True)
            gl_info.all_ld = temp
            lock.release()
        print(gl_info.all_ld[0].index, gl_info.all_ld[0].is_in_android)
        time.sleep(10)


def start_ld_list():
    t = gl_info.ld_list_t
    if t and t.is_alive():
        return
    t = MyThread(target=update_ld_list)
    t.start()
    gl_info.ld_list_t = t
