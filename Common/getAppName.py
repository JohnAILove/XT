# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/27 17:43
@Auth ： 大雄
@File ：getAppName.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import os

from Common.configControl import Config
from Common.雷电模拟器 import Dnconsole
from public import project_path


def create_ld():
    config_path = project_path + "\\Resources\\static\\config.ini"
    config = Config(config_path)
    program_path = config.get_value("全局配置","program_path")
    return Dnconsole(program_path)

def get_ld_app_name(index):
    dn = create_ld()
    return dn.get_activity_name(index)

def push_lib(index,path_dir):
    dn = create_ld()
    for path in os.listdir(path_dir):
        print(dn.adb(index, f"push {path_dir +os.sep +path} /data/local/tmp"))
        print(dn.dnld(index, f"chmod 777 /data/local/tmp/{path}"))

# 转发手机屏幕至http
def send_snapshot(index,prot,width,height):
    dn = create_ld()
    # dn.adb(index, f"forward tcp:{prot} localabstract:minicap")
    dn.dnld(index,f"LD_LIBRARY_PATH=/data/local/tmp /data/local/tmp/minicap -P {width}x{height}@{width}x{height}/0")


def snapshot(index):
    pass

if __name__ == '__main__':
    print(get_ld_app_name(1))
    # push_lib(0, r"E:\code\python\xiaojia_Timo\Resources\static\lib")
    # send_snapshot(0,9000,960,540)