"""
@Time : 2022/7/14 18:47
@Author : 大雄
@Email : 3475228828@qq.com
@func : 雷电相关操作
@lnk : http://bbs.ldmnq.com/forum.php?mod=viewthread&tid=30
"""
import json
import os
import random
import shutil
import threading
import time
from xml.dom.minidom import parseString
import cv2 as cv
import numpy as np


class Dnconsole:

    def __init__(self, console_path):
        # 请根据自己电脑配置
        self.console_path = os.path.dirname(console_path)
        self.console = self.console_path + "\\ldconsole.exe "  # 和dnonsole的区别是一个显示，一个隐藏
        self.ld = self.console_path + "\\ld.exe "
        self.setting_path = self.console_path + "\\vms\\config"
        self.__max_list = None # 存储所有模拟器列表信息
    

    def set_temp_image(self, temp_path):
        self.share_path = temp_path

    # 获取模拟器列表
    def get_list(self, out_ldNums=None,check_=True):
        """
        :param out_ldNums: 排除的模拟器
        :param check:检查第一次和第下次的模拟器数量是否一致
        :return:每个模拟器列表包含：索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        """
        def get_info():
            cmd = os.popen(self.console + 'list2')
            text = cmd.read()
            cmd.close()
            return text.split('\n')
        result = list()
        info = get_info()
        # 是否开启检查数量,避免雷电获取的命令信息有缺
        if check_ and self.__max_list:
            for i in range(10):
                if len(info) ==self.__max_list:
                    break
                else:
                    time.sleep(1)
                    info = get_info()
            else:
                raise "模拟器获取数量不一致"
        else:
            self.__max_list = len(info)

        if len(info)>1:
            info = info[1:] # 去重序号0
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                # 去除模拟器序号
                if out_ldNums and type(out_ldNums) == list:
                    if int(dnplayer[0]) in out_ldNums:
                        continue
                result.append(DnPlayer(dnplayer))
        return result

    # 获取正在运行的模拟器列表
    def list_running(self) -> list:
        result = list()
        all__ = self.get_list()
        for dn in all__:
            if dn.is_running() is True:
                result.append(dn)
        return result

    # 检测指定序号的模拟器是否正在运行
    def is_running(self, index: int) -> bool:
        all__ = self.get_list()
        for item in all__:
            if int(item.index) == index:
                return item.is_in_android

    # 执行shell命令
    def dnld(self, index: int, command: str, silence: bool = True):
        cmd = self.ld + '-s %d %s' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 执行adb命令,不建议使用,容易失控
    def adb(self, index: int, command: str, silence: bool = False) -> str:
        cmd = self.console + 'adb --index %d --command "%s"' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 安装apk 指定模拟器必须已经启动
    def install(self, index: int, path__: str):
        cmd = self.console + 'installapp --index %d --filename %s' % (index, path__)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 卸载apk 指定模拟器必须已经启动
    def uninstall(self, index: int, package: str):
        cmd = self.console + 'uninstallapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 启动App  指定模拟器必须已经启动
    def invokeapp(self, index: int, package: str):
        cmd = self.console + 'runapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 停止App  指定模拟器必须已经启动
    def stopapp(self, index: int, package: str):
        cmd = self.console + 'killapp --index %d --packagename %s' % (index, package)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 输入文字
    def input_text(self, index: int, text: str):
        cmd = self.console + 'action --index %d --key call.input --value %s' % (index, text)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 获取安装包列表
    def get_package_list(self, index: int) -> list:
        result = list()
        text = self.dnld(index, 'pm list packages', False)
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result

    # 检测是否安装指定的应用
    def has_install(self, index: int, package: str):
        if self.is_running(index) is False:
            return False
        return package in self.get_package_list(index)

    # 启动模拟器
    def launch(self, index: int):
        cmd = self.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 关闭模拟器
    def quit(self, index: int):
        cmd = self.console + 'quit --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 重启模拟器，并打开指定应用
    def restart(self,index,packName):
        cmd = self.console + 'action --index %d --key call.reboot --value %s' % (index, packName)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置屏幕分辨率为1080×1920 下次启动时生效
    def set_screen_size(self, index: int, width, hight, dip):
        cmd = self.console + f'modify --index %d --resolution {width},{hight},{dip}' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 点击或者长按某点
    def touch(self, index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            self.dnld(index, 'input tap %d %d' % (x, y))
        else:
            self.dnld(index, 'input touch %d %d %d' % (x, y, delay))

    # 滑动
    def swipe(self, index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            self.dnld(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            self.dnld(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))

    # 复制模拟器,被复制的模拟器不能启动
    def copy(self, name: str, index: int = 0):
        cmd = self.console + 'copy --name %s --from %d' % (name, index)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 添加模拟器
    def add(self, name: str):
        cmd = self.console + 'add --name %s' % name
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 设置自动旋转

    def auto_rate(self, index: int, auto_rate: bool = False):
        rate = 1 if auto_rate else 0
        cmd = self.console + 'modify --index %d --autorotate %d' % (index, rate)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变设备信息 imei imsi simserial androidid mac值

    def change_device_data(self, index: int):
        # 改变设备信息
        cmd = self.console + 'modify --index %d --imei auto --imsi auto --simserial auto --androidid auto --mac auto' % index
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 改变CPU数量
    def change_cpu_count(self, index: int, number: int):
        # 修改cpu数量
        cmd = self.console + 'modify --index %d --cpu %d' % (index, number)
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    def get_cur_activity_xml(self, index: int):
        # 获取当前activity的xml信息
        self.dnld(index, 'uiautomator dump /sdcard/Pictures/activity.xml')
        time.sleep(1)
        f = open(self.share_path + '/activity.xml', 'r', encoding='utf-8')
        result = f.read()
        f.close()
        return result

    def get_user_info(self, index: int):
        xml = self.get_cur_activity_xml(index)
        usr = UserInfo(xml)
        if 'id' not in usr.info:
            return UserInfo()
        return usr

    # 获取当前activity名称
    def get_activity_name(self, index: int):
        text = self.dnld(index, '"dumpsys activity top | grep ACTIVITY"', False)
        text = text.split(' ')
        for i, s in enumerate(text):
            if len(s) == 0:
                continue
            if s == 'ACTIVITY':
                return text[i + 1]
        return ''

    # 等待某个activity出现
    def wait_activity(self, index: int, activity: str, timeout: int) -> bool:
        for i in range(timeout):
            if self.get_activity_name(index) == activity:
                return True
            time.sleep(1)
        return False

    # 找图
    def find_pic(self, index, img_path: str, threshold: float):
        img1 = self.captrue(index)
        img2 = self.imread(img_path)
        # cv.imshow("img1",img1)
        # cv.imshow("img2",img2)
        # cv.waitKey()
        result = cv.matchTemplate(img1, img2, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        # print(max_val)
        yloc, xloc = np.where(result >= threshold)
        if len(xloc):
            return max_loc

    # 自动排序
    def sort(self):
        cmd = self.console + "sortWnd"
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result

    # 修改默认图片保存路径
    def set_sharedPictures(self, index, path):
        set_name = 'statusSettings.sharedPictures'
        new_config = ""  # 写入的文件
        path = path.replace('\\', "/")
        index_setting_path = self.setting_path + "\\leidian%s.config" % index
        with open(index_setting_path, "r+", encoding="utf-8") as fp:
            text = fp.read()
            if set_name in text:
                # 路径已存在，不重复写入
                if path in text:
                    return
                # 参数存在,但是路径不对,替换路径
                else:
                    fp.seek(0)
                    all_line = fp.readlines()
                    for line in all_line:
                        if set_name in line:
                            line = f'\t"{set_name}": "{path}",\n'
                        new_config += line
            # 参数不存在时,使用模板替换文件，并随机在写入部分参数，分辨率默认为960*540*160*240
            else:
                with open(path + "\\leidian_template.config", "r", encoding="utf-8") as fp:
                    new_config = fp.read()
                    new_config = new_config.replace("save_image_path", path)
                    new_config = new_config.replace("phoneIMEI_num", str(Dnconsole.myRandom("int", 12)))
                    new_config = new_config.replace("phoneIMSI_num", str(Dnconsole.myRandom("int", 12)))
                    new_config = new_config.replace("phoneSimSerial_num", str(Dnconsole.myRandom("int", 20)))
                    new_config = new_config.replace("phoneAndroidId_num",
                                                    format(int(Dnconsole.myRandom("hex", 16)), 'x'))
                    new_config = new_config.replace("macAddress_num", format(int(Dnconsole.myRandom("hex", 12)), 'x'))

            # 有更改时,重新写入数据
            with open(index_setting_path, "w", encoding="utf-8") as fp:
                fp.write(new_config)

    # 截图
    def captrue(self, index):
        img_path = f'screencap -p /sdcard/Pictures/apk_scr{index}.png'
        self.dnld(index, img_path)
        return Dnconsole.imread(self.share_path + f"\\apk_scr{index}.png")

    # CV读取图片
    @staticmethod
    def imread(src):
        # 读取图片
        if is_chinese(src):
            img1 = cv.imdecode(np.fromfile(src, dtype=np.uint8), -1)  # 避免路径有中文
        else:
            img1 = cv.imread(src)
        return img1

    # 随机指定类型和长度的整数数字
    @staticmethod
    def myRandom(str_type, len_):
        if str_type == "int":
            multiplier = 10
        elif str_type == "hex":
            multiplier = 16
        min_num = pow(multiplier, len_ - 1)
        max_num = min_num * multiplier - 1
        num = random.randint(min_num, max_num)
        return num


class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])

        try:
            self.name = info[1]
            self.top_win_handler = int(info[2])
            self.bind_win_handler = int(info[3])
            self.is_in_android = True if int(info[4]) == 1 else False
            self.pid = int(info[5])
            self.vbox_pid = int(info[6])
        except:
            self.name = 0
            self.top_win_handler = 0
            self.bind_win_handler = 0
            self.is_in_android = False
            self.pid = 0
            self.vbox_pid = 0

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)

    def __repr__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (
            index, name, twh, bwh, r, pid, vpid)


class UserInfo(object):
    def __init__(self, text: str = ""):
        super(UserInfo, self).__init__()
        self.info = dict()
        if len(text) == 0:
            return
        self.__xml = parseString(text)
        nodes = self.__xml.getElementsByTagName('node')
        res_set = [
            # 用户信息节点
        ]
        name_set = [
            'id', 'id', 'following', 'fans', 'all_like', 'rank', 'flex',
            'signature', 'location', 'video', 'name'
        ]
        number_item = ['following', 'fans', 'all_like', 'video', 'videolike']
        for n in nodes:
            name = n.getAttribute('resource-id')
            if len(name) == 0:
                continue
            if name in res_set:
                idx = res_set.index(name)
                text = n.getAttribute('text')
                if name_set[idx] not in self.info:
                    self.info[name_set[idx]] = text
                    print(name_set[idx], text)
                elif idx == 9:
                    self.info['videolike'] = text
                elif idx < 2:
                    if len(text) == 0:
                        continue
                    if self.info['id'] != text:
                        self.info['id'] = text
        for item in number_item:
            if item in self.info:
                self.info[item] = int(self.info[item].replace('w', '0000').replace('.', ''))

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return str(self.info)


# 判断字符串是否为中文
def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


if __name__ == '__main__':
    # path = r"D:\leidian\LDPlayer9\ld.exe"
    path = r"F:\LDPlayer\LDPlayer3.0\dnplayer.exe"
    dn = Dnconsole(path)
    dn.dnld(0,"forward tcp:1717 localabstract:minicap")
