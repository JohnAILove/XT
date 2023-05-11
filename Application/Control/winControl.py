# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/18 21:55
@Auth ： 大雄
@File ：winControl.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import sys
import time
import traceback

from Application.Control.processControl import processControl

from Common.gamePlugIn import GamePlugIn
from Common.publicFunction import *


def winControl(row_num):
    # 设置游戏插件
    ldNum = gl_info.all_ld[row_num].index
    ld = gl_info.ld
    ld.set_temp_image(temp_image_path)
    gp = GamePlugIn(ldNum, ld)
    image_path = get_script_value(gl_info.script, "resources_path") + f"image\\"
    gp.set_image(image_path)

    # 回写数据
    td_info[row_num].gp = gp
    td_info[row_num].restart_num = restart_num
    gl_info.ms = get_script_value(gl_info.script, "ms")
    gl_info.loc = get_script_value(gl_info.script, "loc")
    gl_info.resources_path = get_script_value(gl_info.script, "resources_path")
    # TSN脚本的回写
    if gl_info.script == "TSN":
        gl_info.tsn_token = int(gl_info.mainView.lineEdit_3.text())
        gl_info.fuli_state = gl_info.mainView.radioButton_fuli.isChecked()
        gl_info.bubing = gl_info.mainView.radioButton_bubing.isChecked()
        gl_info.meiri = gl_info.mainView.radioButton_meiri.isChecked()
    # 启动流程
    if debug:
        try:
            processControl(row_num)
        except Exception as E:
            try:
                progress = td_info[row_num].progress
                gl_info.csv.edit_cell(row_num + 1, 6, str[progress])
            except Exception as e:
                update_log(f"td_info[row_num].progress报错,报错代码 {e}", row_num)
            update_task(row_num, "报错")
            update_log(f"报错代码 {E}", row_num)
            update_log(str(sys.exc_info()),row_num)
            update_log(traceback.format_exc(),row_num)
    else:
        processControl(row_num)


    # 关闭模拟器
    update_log("流程结束,关闭模拟器",row_num)
    ld.quit(ldNum)
    # 存活模拟器-1
    gl_info.queue_num -= 1
