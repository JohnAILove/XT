# -*- coding: utf-8 -*-
"""
@Time ： 2022/11/29 14:12
@Auth ： 大雄
@File ：my_thread.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import ctypes
import threading


class MyThread(threading.Thread):
    handle = None

    def __init__(self, target=None, args=(), kwargs=None,daemon=True):
        super(MyThread, self).__init__(target=target, args=args, kwargs=kwargs,daemon=daemon)
        self.flag = threading.Event()


    # 虽然能停止线程,但是线程计数并没有减少,会有不可预知的问题
    def stop(self):
        if not self.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.ident), exc)
        if res == 0:
            raise ValueError("找不到线程ID")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise SystemError("线程已停止")

