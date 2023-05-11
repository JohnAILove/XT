"""
@Time : 2022/7/4 14:53
@Author : Administrator
@Email : 3475228828@qq.com
@Project : 主界面视图
"""
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from Resources.ui.untitled import Ui_Form
import os
import sys
import win32com.client


class MainView(Ui_Form, QWidget):
    def __init__(self):
        super(MainView, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        self.menu = QMenu()
        self.ui_init()
        # 拖入事件
        self.setAcceptDrops(True)
        # self.installEventFilter(self)

    def ui_init(self):
        """ ui自定义样式 """
        # 第0行和标题加横杠--
        self.tableWidget.horizontalHeader().setStyleSheet(
            "border-bottom-width: 0.5px;border-style: outset;border-color: rgb(229,229,229);"
        )
        self.tableWidget.verticalHeader().hide()  # 隐藏左侧序号
        # self.pushButton_10.setEnabled(False)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        # 判断有没有接受到内容
        if a0.mimeData().hasUrls():
            # 如果接收到内容了，就把它存在事件中
            a0.accept()
        else:
            # 没接收到内容就忽略
            a0.ignore()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        if a0:
            for i in a0.mimeData().urls():
                file_path = i.path()[1:]
                if file_path[-3:] == "lnk":
                    # self.lineEdit.setText(file_path)
                    # 获取lnk数据
                    shell = win32com.client.Dispatch("WScript.Shell")
                    shortcut = shell.CreateShortCut(file_path)
                    file_path = shortcut.Targetpath
                    self.lineEdit.setText(file_path)
                    print(file_path)
                    break


    # 一键启动，禁止模拟器按键点击
    def show_mn(self, state,flag):
        if state == "auto":
            self.pushButton.setEnabled(flag)
            self.pushButton_2.setEnabled(flag)
            self.pushButton_4.setEnabled(flag)
            self.pushButton_5.setEnabled(flag)

            # self.pushButton_9.setEnabled(flag)
            self.pushButton_11.setEnabled(flag)
            self.pushButton_12.setEnabled(flag)
            self.pushButton_13.setEnabled(flag)
            self.pushButton_14.setEnabled(flag)

            if flag:
                self.pushButton_6.setEnabled(True)
                self.pushButton_10.setEnabled(False)
            else:
                self.pushButton_6.setEnabled(False)
                self.pushButton_10.setEnabled(True)
        #
        # if state == "run_mn":
        #     if flag:
        #         self.pushButton_6.setEnabled(True)
        #         self.pushButton_10.setEnabled(False)
        #     else:
        #         self.pushButton_6.setEnabled(False)
        #         self.pushButton_10.setEnabled(False)

    # 隐藏吞噬币提交数量label和line空间
    def hide_tsn(self,flag=False):
        if flag:
            self.label_5.show()
            self.lineEdit_3.show()
            self.radioButton_fuli.show()
            self.radioButton_bubing.show()
        else:
            self.label_5.hide()
            self.lineEdit_3.hide()
            self.radioButton_fuli.hide()
            self.radioButton_bubing.hide()

    # 错误告警框
    def show_message(self,title,content):
        QMessageBox.critical(self, str("title"), str(content))