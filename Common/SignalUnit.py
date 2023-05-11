# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : SignalUnit.py
# Time       ：22/3/6 11:33
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：界面回写信号量
"""

from PyQt5.Qt import QObject, pyqtSignal

class SignalUnit(QObject):
    table = pyqtSignal(int, int, str)
    log = pyqtSignal(str)
signal = SignalUnit()

