# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/17 21:01
@Auth ： 大雄
@File ：mainControl.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""
import time

from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt

from Application.Control.threadControl import ThreadControl
from Application.Control.threadSonControl import start_ld_list
from Common.publicFunction import *
from Application.View.mainView import MainView
from Common.SignalUnit import signal
from Common.configControl import Config
from Common.publicFunction import update_log
from public import *


class MainController:
    # """初始化加载配置等"""
    def __init__(self):
        self.account_list = []
        self.ini = path + "config.ini"
        self.mainView = MainView()
        gl_info.mainView = self.mainView
        self.load_settings()
        self.event_int()

        self.mainView.show()
        self.set_comboBox()

    # 事件
    def event_int(self):
        self.mainView.pushButton.clicked.connect(lambda: self.run_mn("one",True))
        self.mainView.pushButton_2.clicked.connect(lambda: self.run_mn("all",True))
        self.mainView.pushButton_3.clicked.connect(self.open_log)

        self.mainView.pushButton_4.clicked.connect(lambda: self.run_mn("one",False))
        self.mainView.pushButton_5.clicked.connect(lambda: self.run_mn("all",False))
        self.mainView.pushButton_6.clicked.connect(self.start_auto)
        self.mainView.pushButton_7.clicked.connect(self.get_mn_list)
        self.mainView.pushButton_8.clicked.connect(self.save_settings)
        self.mainView.pushButton_9.clicked.connect(self.sort_auto)
        self.mainView.pushButton_10.clicked.connect(self.stop_auto)
        self.mainView.pushButton_11.clicked.connect(self.init_mn)
        self.mainView.pushButton_12.clicked.connect(self.installAPP)
        self.mainView.pushButton_13.clicked.connect(lambda: self.script("stop"))
        self.mainView.pushButton_14.clicked.connect(lambda: self.script("run"))

        # 下拉框事件
        self.mainView.comboBox.currentIndexChanged.connect(self.set_comboBox)

        # 信号
        signal.table.connect(self.display_status)
        signal.log.connect(self.display_log)

    """加载配置"""
    def load_settings(self):

        if os.path.exists(self.ini):
            settings = Config(self.ini)
            section = "全局配置"
            program_path = settings.get_value(section, "program_path")  # 模拟器路径

            simulators_num = settings.get_value(section, "simulators_num")  # 同时存在模拟器数量
            simulators_num = str(simulators_num) if simulators_num else simulators_num

            start_delay = settings.get_value(section, "start_delay")  # 启动间隔
            start_delay = str(start_delay) if start_delay else start_delay

            out_ldNum = settings.get_value(section,"out_ldNum")  # 排除模拟器序号,已列表的形式
            out_ldNum = str(out_ldNum) if out_ldNum else out_ldNum

            script_index = settings.get_value(section,"script_index")
            script_index = int(script_index) if script_index else 0  # 默认选择框第一个,Timo脚本

            tsn_token = settings.get_value(section,"tsn_token")
            tsn_token = tsn_token if tsn_token else "50"

            fuli_state = settings.get_value(section,"fuli_state")
            fuli_state = True if "True" == fuli_state else False
            bubing_state = settings.get_value(section,"bubing_state")
            bubing_state = True if "True" == bubing_state else False
            meiri_state = settings.get_value(section,"meiri_state")
            meiri_state = True if "True" == meiri_state else False
            # 显示界面
            self.mainView.lineEdit.setText(program_path)
            self.mainView.lineEdit_2.setText(simulators_num)
            self.mainView.lineEdit_3.setText(tsn_token)
            self.mainView.lineEdit_4.setText(out_ldNum)
            self.mainView.lineEdit_5.setText(start_delay)
            self.get_mn_list()
            self.mainView.comboBox.setCurrentIndex(script_index)
            self.mainView.radioButton_fuli.setChecked(fuli_state)
            self.mainView.radioButton_bubing.setChecked(bubing_state)
            self.mainView.radioButton_meiri.setChecked(meiri_state)

    # 获取模拟器序号列表,并显示
    def get_mn_list(self):
        self.account_list = []
        path = self.mainView.lineEdit.text()
        if "exe" in path:
            gl_info.ld = get_ld_object(path)
            gl_info.out_ldNum = out_ldNumF(self.mainView.lineEdit_4.text())
            start_ld_list()
            time.sleep(1)
            res = gl_info.all_ld
            if res:
                for item in res:
                    self.account_list.append([item.index, item.bind_win_handler, item.is_in_android])
                self.load_account()


    # """加载模拟器列表界面"""
    def load_account(self):
        # 清空
        self.mainView.tableWidget.clearContents()
        # 用户列表是否存在
        if self.account_list:
            row = len(self.account_list)
            self.mainView.tableWidget.setRowCount(row)
            for table_line, user_line in enumerate(self.account_list):
                newItem = QTableWidgetItem(str(user_line[0]))
                newItem1 = QTableWidgetItem(str(user_line[1]))
                newItem2 = QTableWidgetItem(str(user_line[2]))

                self.mainView.tableWidget.setItem(table_line, 0, newItem)  # 显示
                self.mainView.tableWidget.setItem(table_line, 1, newItem1)  # 显示
                self.mainView.tableWidget.setItem(table_line, 2, newItem2)  # 显示
                # self.mainView.tableWidget.setItem(table_line, 3, newItem3)  # 显示

                newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中
                newItem1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中
                newItem2.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中
                # newItem3.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中

    # """保存界面配置"""
    def save_settings(self):
        # 初始化
        settings = Config(self.ini)
        section = "全局配置"
        settings.add_section(section)
        # 获取数据
        program_path = self.mainView.lineEdit.text()
        simulators_num = self.mainView.lineEdit_2.text()
        tsn_token = self.mainView.lineEdit_3.text()
        out_ldNum = self.mainView.lineEdit_4.text()
        start_delay = self.mainView.lineEdit_5.text()

        script_index = self.mainView.comboBox.currentIndex()
        fuli_state = str(self.mainView.radioButton_fuli.isChecked())
        bubing_state = str(self.mainView.radioButton_bubing.isChecked())
        meiri_state = str(self.mainView.radioButton_meiri.isChecked())

        # 写入数据
        settings_dict = {
            "program_path": program_path,
            "simulators_num": simulators_num,
            "start_delay": start_delay,
            "out_ldNum":out_ldNum,
            "script_index":script_index,
            "tsn_token":tsn_token,
            "fuli_state": fuli_state,
            "bubing_state":bubing_state,
            "meiri_state":meiri_state,
        }
        for k, v in settings_dict.items():
            if not v and v != 0: # 排除数字0
                v = ''
            settings.set(section, str(k), str(v))
        settings.write()
        update_log("已保存配置")

    # 读取用户界面列表
    def read_account_list(self):
        self.account_list = []
        count = self.mainView.tableWidget.rowCount()
        if count:
            for line in range(count):
                index = self.mainView.tableWidget.item(line, 0).text()
                hwnd = self.mainView.tableWidget.item(line, 1).text()
                run = self.mainView.tableWidget.item(line, 2).text()
                self.account_list.append([index, hwnd, run])
            return self.account_list

    # 启动或者关闭模拟器
    def run_mn(self, flag,bool_):
        row_num = -1
        if flag == "one":
            for i in self.mainView.tableWidget.selectionModel().selection().indexes():
                num = i.row()
                # 去重
                if row_num != num:
                    row_num = num
                    if bool_:
                        ThreadControl().start_ld(row_num)
                    else:
                        ThreadControl().stop_ld(row_num)

        elif flag == "all":
            count = self.mainView.tableWidget.rowCount()
            row_nums = range(count) if count else []
            delay = self.mainView.lineEdit_5.text()
            delay = int(delay) if delay else 0
            if bool_:
                ThreadControl().start_all_ld(row_nums,delay)
            else:
                ThreadControl().stop_all_ld(row_nums)

    # 一键启动
    def start_auto(self):
        row_nums = self.mainView.tableWidget.rowCount()
        row_nums = range(row_nums) if row_nums else []
        delay = self.mainView.lineEdit_5.text()
        delay = int(delay) if delay else None
        simulators_num = self.mainView.lineEdit_2.text()
        simulators_num = int(simulators_num) if simulators_num else None

        ThreadControl().start_all(row_nums,delay,simulators_num)
        # 设置启动模拟器，关闭模拟器，停止脚本，启动脚本，不可点击
        # self.mainView.show_mn("auto",False)

    # 一键停止
    def stop_auto(self):
        # simulators_num = self.mainView.lineEdit_2.text()
        # start_delay = self.mainView.lineEdit_5.text()
        # ThreadUnit(simulators_num, start_delay).stop_thread()
        ThreadControl().stop_all()
        self.mainView.show_mn("auto", True)


    def display_status(self, row, column, content):
        """ 线程状态更新 """
        newItem = QTableWidgetItem(content)
        self.mainView.tableWidget.setItem(row, column, newItem)
        newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)  # 居中显示

    def display_log(self, content):
        """ 日志打印 """
        self.mainView.textBrowser.append(content)
        self.mainView.textBrowser.ensureCursorVisible()

    def sort_auto(self):
        ThreadControl.sort()

    # 初始化模拟器
    def init_mn(self):
        count = self.mainView.tableWidget.rowCount()
        row_nums = range(count) if count else  []
        ThreadControl.init_ld(row_nums)

    def installAPP(self):
        row_num = -1
        ld = get_ld_object(self.mainView.lineEdit.text())
        out_ldNum = out_ldNumF(self.mainView.lineEdit_4.text())
        for i in self.mainView.tableWidget.selectionModel().selection().indexes():
            num = i.row()
            # 去重
            if row_num != num:
                row_num = num
                lis = ld.get_list(out_ldNum)
                ldNum = lis[row_num].index
                if lis and lis[row_num].is_in_android:
                    apk_path = get_script_value(gl_info.script,"apk_name")
                    update_log(f"正在安装apk",row_num)
                    ld.install(ldNum,apk_path)
                    update_log(f"已安装apk",row_num)
                    # 回写数据
                    gl_info.out_ldNum = out_ldNum
                    gl_info.all_ld = lis
                else:
                    update_log("请启动模拟器",row_num)
                    break

    # 启动或者关闭脚本
    def script(self,flag):
        row_num = -1
        for i in self.mainView.tableWidget.selectionModel().selection().indexes():
            num = i.row()
            # 去重
            if row_num != num:
                row_num = num
                if flag == "run":
                    ThreadControl().start(row_num)
                else:
                    ThreadControl().stop(row_num)

    def set_comboBox(self):
        gl_info.script = self.mainView.comboBox.currentText()
        update_log(f"当前选择脚本为: {gl_info.script}")
        gl_info.resources_path = get_script_value(gl_info.script,"resources_path")
        if gl_info.script == "TSN":
            self.mainView.hide_tsn(True)
            # 初始化csv文本
            csv_name = get_script_value(gl_info.script,"csv_name")
            csv_f = self.mainView.lineEdit.text()[:3]
            key_list = []
            if gl_info.all_ld:
                for i in gl_info.all_ld:
                    key_list.append(i.index)
            csv_init(csv_f+csv_name,key_list)
            # 回写界面状态
            gl_info.csv.set_key(0)
            for row_num,ldNum in enumerate(key_list):
                content = gl_info.csv.get_value(ldNum)
                if not content:
                    self.mainView.show_message("error",f"模拟器有新增,请删除csv文件：{csv_name}")
                if len(content)>6:
                    update_task(row_num,content[6])

        else:
            self.mainView.hide_tsn(False)

    def open_log(self):
        row_num = -1
        for i in self.mainView.tableWidget.selectionModel().selection().indexes():
            num = i.row()
            # 去重
            if row_num != num:
                row_num = num
                ldNum = gl_info.all_ld[row_num].index
                cmd = "start " + gl_info.resources_path + "log/%s" % ldNum + '.txt'
                os.system(cmd)


