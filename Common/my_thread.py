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
from ctypes import wintypes


class _MyThread:

    def __init__(self, target=None, args=(), kwargs={}):
        # 定义数据类型
        self.__handle = None
        self.__is_stopped = 0
        self.__exit_code = 0
        self.__run_code = 259
        # win32api
        self.__kernel32 = ctypes.windll.kernel32
        self.__CreateThread = self.__kernel32.CreateThread
        self.__CloseHandle = self.__kernel32.CloseHandle
        self.__WaitForSingleObject = self.__kernel32.WaitForSingleObject
        self.__WaitForSingleObject.argtypes = wintypes.HANDLE, wintypes.DWORD
        self.__WaitForSingleObject.restype = wintypes.DWORD

        def check_handle(result, func, args):
            if result is None:
                raise ctypes.WinError(ctypes.get_last_error())
            return args

        def check_bool(result, func, args):
            if not result:
                raise ctypes.WinError(ctypes.get_last_error())
            return None

        # 定义CreateThread函数api的参数类型和回调函数参数类型和返回类型
        wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
        wintypes.SIZE_T = ctypes.c_size_t
        LPSECURITY_ATTRIBUTES = ctypes.c_void_p
        LPTHREAD_START_ROUTINE = ctypes.WINFUNCTYPE(None)
        self.__CreateThread.errcheck = check_handle
        self.__CreateThread.restype = wintypes.HANDLE
        self.__CreateThread.argtypes = (
            LPSECURITY_ATTRIBUTES,  # _In_opt_  lpThreadAttributes
            wintypes.SIZE_T,  # _In_      dwStackSize
            LPTHREAD_START_ROUTINE,  # _In_      lpStartAddress
            wintypes.LPVOID,  # _In_opt_  lpParameter
            wintypes.DWORD,  # _In_      dwCreationFlags
            wintypes.LPDWORD,  # _Out_opt_ lpThreadId
        )
        self.__CloseHandle.errcheck = check_bool
        self.__CloseHandle.argtypes = (wintypes.HANDLE,)

        # CreateThread函数参数
        self.lpThreadAttributes = None  # 参数1：lpThreadAttributes,指向SECURITY_ATTRIBUTES型态的结构的指针,NULL使用默认安全性，不可以被子线程继承，否则需要定义一个结构体将它的bInheritHandle成员初始化为TRUE
        self.dwStackSize = 0  # 参数2:dwStackSize,设置初始栈的大小，以字节为单位，如果为0，那么默认将使用与调用该函数的线程相同的栈空间大小。任何情况下，Windows根据需要动态延长堆栈的大小。
        self.lpStartAddress = LPTHREAD_START_ROUTINE(
            lambda: target(*args, **kwargs))  # 参数3:lpStartAddress，指向线程函数的指针，形式：@函数名，函数名称没有限制，
        self.param = None  # 参数4:lpParameter：向线程函数传递的参数，是一个指向结构的指针，不需传递参数时，为NULL。
        self.dwCreationFlags = 4  # 0x00000000 开始线程 # 0x00000004 挂起线程 #  0x00010000后台线程
        self.tid = ctypes.byref(wintypes.DWORD())  # 参数6:lpThreadId:保存新线程的id。
        self.__handle = self.__CreateThread(self.lpThreadAttributes,
                                            self.dwStackSize,
                                            self.lpStartAddress,
                                            self.param,
                                            self.dwCreationFlags,
                                            self.tid)
        if self.dwCreationFlags == 4:
            self.__is_stopped = 1

    def __thread_state(self):
        state_id = wintypes.DWORD()
        if self.__kernel32.GetExitCodeThread(self.__handle, ctypes.byref(state_id)):
            return state_id.value
        return 0

    def start(self):
        if self.__handle:
            self.__kernel32.ResumeThread(self.__handle)

    def pause(self):
        if self.is_alive() and self.__is_stopped == 1:
            print("暂停线程")
            if self.__kernel32.SuspendThread(self.__handle) != -1:
                self.__is_stopped = 0

    def resume(self):
        if self.is_alive() and self.__is_stopped == 0:
            print("恢复线程")
            if self.__kernel32.ResumeThread(self.__handle) != -1:
                self.__is_stopped = 1

    def stop(self):
        if self.is_alive():
            print("停止线程")
            self.__TerminateThread() # 停止线程
            self.__WaitForSingleObject(self.__handle, 1000) # 等待线程关闭
            if self.__thread_state() == self.__exit_code: # 确认退出
                self.__CloseHandle(self.__handle)  # 关闭内壳，如果线程正常退出，也会自动关闭。
                self.__handle = None
                self.__is_stopped = 0
            else:
                raise "线程无法停止"

    def __TerminateThread(self):
        self.__kernel32.TerminateThread(self.__handle,0)

    def __ExitThread(self):
        self.__kernel32.ExitThread(0)

    def is_alive(self):
        if self.__thread_state() == self.__run_code: return True
        return False


class MyThread(threading.Thread):
    handle = None

    def __init__(self, target=None, args=(), kwargs=None,daemon=True):
        super(MyThread, self).__init__(target=target, args=args, kwargs=kwargs,daemon=daemon)


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

#



#
# def thread_son_test(num):
#     for i in range(num):
#         time.sleep(0.3)
#         print(i)
#
#
# def thread_test(num1):
#     t1 = MyThread(target=thread_son_test, args=(10,))
#     t1.start()
#
#
# class DMInput():
#     winKernel32 = ctypes.windll.kernel32
#     winuser32 = ctypes.windll.LoadLibrary('user32.dll')
#
#     @staticmethod
#     def MoveTo(x, y) -> None:
#         MOUSEEVENTF_MOVE = 0x0001
#         MOUSEEVENTF_ABSOLUTE = 0x8000
#         SM_CXSCREEN = 0
#         SM_CYSCREEN = 1
#         cx_screen = DMInput.winuser32.GetSystemMetrics(SM_CXSCREEN)
#         cy_screen = DMInput.winuser32.GetSystemMetrics(SM_CYSCREEN)
#         real_x = round(65535 * x / cx_screen)
#         real_y = round(65535 * y / cy_screen)
#         DMInput.winuser32.mouse_event(MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE, real_x, real_y, 0, 0)


# if __name__ == '__main__':
#     t1 = MyThread(target=thread_son_test, args=(100,))
#     t1.start()
#     t1.pause()
#     time.sleep(2)
#     t1.resume()
#     time.sleep(2)
#     t1.pause()
#     time.sleep(2)
#     t1.resume()
#     t1.pause()
#     t1.resume()
#     t1.stop()
#     input()
