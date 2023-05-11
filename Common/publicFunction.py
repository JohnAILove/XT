# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/18 17:57
@Auth ： 大雄
@File ：publicFunction.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
from Common.SignalUnit import signal
from Common.config_csv import CSV
from Common.雷电模拟器 import Dnconsole
from public import *


def update_ld_hwnd(row_num, content):
    signal.table.emit(row_num, 1, str(content))


def update_ld_run(row_num, content):
    signal.table.emit(row_num, 2, str(content))

def update_task(row_num, content):
    signal.table.emit(row_num, 3, str(content))

def update_log(content, row_num=None):
    if not row_num is None:
        ldNum = gl_info.all_ld[row_num].index
        signal.log.emit(f"{ldNum}:{str(content)} \n")
        # 写入日志
        name = "%s" % ldNum + ".txt"
        new_path = gl_info.resources_path + "log\\%s" % name
        with open(new_path, "a+", encoding="utf8") as fp:
            now_time = time.time()
            now_time = time.localtime(now_time)
            now_time = time.strftime("%Y-%m-%d %H:%M:%S  ", now_time)
            fp.write(now_time + content + "\n")
    else:
        signal.log.emit(str(content) + "\n")




# 获取任务状态
def get_task_state():
    states = []
    count = gl_info.mainView.tableWidget.rowCount()
    for line in range(count):
        try:
            state = gl_info.mainView.tableWidget.item(line, 3).text()
            if state != "任务完成":
                states.append(line)
        except AttributeError as e:
            print("无法获取表格第第四列数据")
    return states


# 获取属性
def get_script_value(script_name, key):
    k = getattr(Script_public, script_name)
    return getattr(k, key)


# 初始化csv
def csv_init(path,key_list):
    line_first = ["模拟器编号", "登入好礼天数", "登入好礼>=14天↑", "吞食币数量", "已上传交易市集", "应剩余吞食币",
                  f"模拟器数{len(key_list)},任务完成情况",]
    if os.path.exists(path):
        update_log("# 遍历更新表格")
        csv = CSV(path)
        now_key_list = csv.get_column(0)

        # 写入表头
        csv.edit(0,line_first)
        # 对比表格长度是否一致,如果表格内容少于模拟器数量,则添加空数据
        if len(now_key_list) < len(key_list) + 1:
            update_log("表格行数不一致,正在补齐数据")
            for key in range(len(now_key_list),len(key_list) + 1):
                update_log(f"表格第{key}行添加初始化数据")
                csv.add([key, 0, False, 0, 0, 0,"未启动"])
        else:
            update_log("# 模拟器未新增,表格行数一致,不新增")

    else:
        csv = CSV(path)
        update_log("创建表格")
        update_log("创建表头 %s"%line_first)
        csv.add(line_first)
        for row,key in enumerate(key_list):
            update_log(f"创建第{row+1}行 数据初始化")
            csv.add([key, 0, False, 0, 0, 0,"未启动"])
    gl_info.csv = csv


# 获取雷电对象
def get_ld_object(path=None):
    if path:
        if path != gl_info.ld_path:
            gl_info.ld = Dnconsole(path)
            gl_info.ld_path = path
    elif not gl_info.ld:
        raise "参数有误,请填写雷电路径"
    return gl_info.ld

# 排除雷电序号
def out_ldNumF(out_ldNum):
    if out_ldNum:
        out_ldNum = eval(out_ldNum)
        if type(out_ldNum) == str:
            return out_ldNum.split(",")
        elif type(out_ldNum) == list:
            return list(range(out_ldNum[0],out_ldNum[1]))
        elif type(out_ldNum) == tuple:
            return list(out_ldNum)
        else:
            update_log(f"填写 排除序号{out_ldNum} 错误")

