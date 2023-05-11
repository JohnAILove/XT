# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/20 23:44
@Auth ： 大雄
@File ：threadControl.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import copy
import time

from Application.Control.threadSonControl import stop_one_thread
from Application.Control.winControl import winControl
from Application.model.model import td_info, gl_info
from Common.my_thread import MyThread
from Common.publicFunction import update_log, update_ld_run, update_ld_hwnd, get_ld_object, get_task_state
from public import ld_ratio, temp_image_path


class ThreadControl:
    def __init__(self):
        pass

    @staticmethod
    def __init_ld(row_nums):
        for row_num in row_nums:
            ThreadControl().set_size(row_num,*ld_ratio)
            ThreadControl().set_capture_path(row_num,temp_image_path)


    # 初始化模拟器
    @staticmethod
    def init_ld(row_nums):
        t = gl_info.init_ld
        if t and t.is_alive():
            return update_log("正在初始化中",-1)
        t = MyThread(target=ThreadControl.__init_ld,args=(row_nums,))
        t.start()
        gl_info.init_ld = t

    @staticmethod
    def sort():
        get_ld_object(gl_info.mainView.lineEdit.text()).sort()
        update_log("一键排序已完成")

    @staticmethod
    def set_size(row_num, width, height, dpi):
        update_log(f"设置分辨率{width, height, dpi}", row_num)
        ldNum = gl_info.all_ld[row_num].index
        gl_info.ld.set_screen_size(ldNum, width, height, dpi)

    # 设置截图保存路径
    @staticmethod
    def set_capture_path(row_num, path):
        update_log(f"设置截图路径", row_num)
        ldNum = gl_info.all_ld[row_num].index
        gl_info.ld.set_sharedPictures(ldNum, path)

    def task(self, row_num):
        # 判断模拟器是否启动,如果未启动,则启动模拟器
        if not gl_info.all_ld[row_num].is_in_android:
            self.__start_ld(row_num)
        self.sort()
        winControl(row_num)

    def __start_ld(self, row_num):
        if gl_info.all_ld[row_num].is_in_android:
            update_log(f"模拟器已启动", row_num)
            return

        gl_info.ld.launch(gl_info.all_ld[row_num].index)
        update_log(f"模拟器启动中...", row_num)
        update_ld_run(row_num, "启动中")

        # 等待模拟器状态一致
        for i in range(100):
            time.sleep(1)
            if gl_info.all_ld[row_num].is_in_android:
                break
        else:
            update_log("启动失败,请手动启动", row_num)

        # 回写界面
        update_ld_run(row_num, True)
        update_ld_hwnd(row_num, gl_info.all_ld[row_num].bind_win_handler)
        update_log(f"模拟器启动成功", row_num)

    def __stop_ld(self, row_num):
        t = td_info[row_num].ld_t
        while True:
            if t and t.is_alive():
                if gl_info.all_ld[row_num].is_in_android:
                    gl_info.ld.quit(gl_info.all_ld[row_num].index)
                    update_log("雷电线程已停止", row_num)
                    break
                else:
                    update_log("模拟器启动过程中,等待启动完成自动关闭")
                    time.sleep(1)
            else:
                gl_info.ld.quit(gl_info.all_ld[row_num].index)
                update_log("雷电线程已停止", row_num)
                break
        update_ld_run(row_num,"False")

    def __start_all_ld(self, row_nums, start_delay):
        update_log("启动所有模拟器")
        for row_num in row_nums:
            self.__start_ld(row_num)
            time.sleep(float(start_delay))

    def start_ld(self, row_num):
        t = td_info[row_num].ld_t
        if t and t.is_alive():
            return update_log("雷电线程启动中", row_num)
        t = MyThread(target=self.__start_ld, args=(row_num,))
        t.start()
        # 回写数据
        td_info[row_num].ld_t = t

    def pause_ld(self):
        pass

    def resume(self):
        pass

    def stop_ld(self, row_num):
        update_log("关闭模拟器", row_num)
        t = td_info[row_num].ld_stop_t
        if t and t.is_alive():
            return update_log("雷电线程正在停止中", row_num)
        t = MyThread(target=self.__stop_ld, args=(row_num,))
        t.start()
        td_info[row_num].ld_stop_t = t

    def start_all_ld(self, row_nums, delay):
        update_log("启动所有模拟器")
        t = gl_info.all_ld_t
        if t and t.is_alive():
            return update_log("所有模拟器启动中,请等待启动完成")
        t = MyThread(target=self.__start_all_ld, args=(row_nums, delay))
        t.start()
        gl_info.all_ld_t = t

    def stop_all_ld(self, row_nums):
        update_log("停止所有雷电模拟器", -1)
        t = gl_info.all_ld_t
        if t:
            t.stop()
        for row_num in row_nums:
            self.stop_ld(row_num)

    def __start(self, row_num):
        update_log("启动脚本", row_num)
        t = td_info[row_num].thread
        if t and t.is_alive():
            update_log("线程正在运行中", row_num)
        else:
            thread = MyThread(target=self.task, args=(row_num,))
            update_log("启动线程", row_num)
            # 回写数据
            # td_info[row_num].dm = DM()
            # td_info[row_num].py = py
            td_info[row_num].thread = thread
            td_info[row_num].thread_status = 0
            gl_info.row_nums.append(row_num)
            # 启动线程
            thread.start()

    def __start_all_thread(self, row_nums, start_delay,simulators_num):
        update_log("启动所有脚本")
        lines = get_task_state()
        lines2 = copy.deepcopy(lines)
        ldNums = [gl_info.all_ld[row_num].index for row_num in lines2]
        update_log(f"任务队列为:{ldNums}")
        while True:
            gl_info.row_nums = lines2
            time.sleep(1)
            if not lines:
                update_log("已无等待队列")
                break
            if gl_info.queue_num <simulators_num:
                gl_info.queue_num +=1
                row_num = lines.pop(0)
                self.start(row_num)
                time.sleep(int(start_delay))
        # 检测是否有活动线程
        while True:
            time.sleep(2)
            for row_num in lines2:
                if td_info[row_num].thread:
                    break
            else:
                return update_log("一键启动已完成")
                gl_info.mainView.show_mn("auto",True)

    def start(self, row_num):
        self.__start(row_num)

    def stop(self, row_num):
        stop_one_thread(row_num)
        self.stop_ld(row_num)

    def pause(self):
        pass

    def resume(self):
        pass

    def start_all(self, row_nums, start_delay, simulators_num):
        t_all = MyThread(target=self.__start_all_thread, args=(row_nums, start_delay,simulators_num))
        t_all.start()
        # 回写数据
        gl_info.t_all = t_all

    def stop_all(self):
        update_log("停止所有")
        gl_info.t_all.stop()
        for row_num in gl_info.row_nums:
            self.stop(row_num)
            time.sleep(0.05)
