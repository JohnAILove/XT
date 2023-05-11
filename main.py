# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/17 20:57
@Auth ： 大雄
@File ：main.py
@IDE ：PyCharm
@Email:3475228828@qq.com
"""

import sys
from PyQt5.QtWidgets import QApplication
from Application.Control.mainControl import MainController


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 运行窗口
    main_ui = MainController()
    # 运行结束
    sys.exit(app.exec_())