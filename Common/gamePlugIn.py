# -*- coding: utf-8 -*-
"""
@Time ： 2023/1/27 21:03
@Auth ： 大雄
@File ：gamePlugIn.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import ctypes
import os.path
import time

import numpy as np
import cv2

from Common.雷电模拟器 import Dnconsole
from public import Script_public
from public import dll

class GamePlugIn:
    def __init__(self, ldNum, obj):
        self.ldNum = ldNum
        self.obj = obj
        self.ocr_path = None
        self.image_dir = None  # 特征图片目录
        self.image_path = self.obj.share_path + f"\\apk_scr{ldNum}.png"  # 雷电截图图片路径

    # 颜色格式ffffff-303030 转cv格式遮罩范围(100,100,100),(255,255,255)
    # 转换大漠格式RGB "ffffff-303030" 为 BGR遮罩范围(100,100,100),(255,255,255)
    def __color_to_range(self, color, sim=1):
        if sim <= 1:
            if len(color) == 6:
                c = color
                weight = "000000"
            elif not color:
                lower = [0,0,0]
                upper = [0,0,0]
                return lower,upper
            elif "-" in color:
                c, weight = color.split("-")
            else:
                raise "参数错误"
        else:
            raise "参数错误"
        # color = int(c[:2], 16), int(c[4:], 16), int(c[2:4], 16)
        # weight = int(weight[:2], 16), int(weight[2:4], 16), int(weight[4:], 16)
        color = int(c[4:], 16), int(c[2:4], 16), int(c[:2], 16)
        weight = int(weight[4:], 16), int(weight[2:4], 16), int(weight[:2], 16)
        sim = int((1 - sim) * 255)
        lower = tuple(map(lambda c, w: max(0, c - w - sim), color, weight))
        upper = tuple(map(lambda c, w: min(c + w + sim, 255), color, weight))
        return lower, upper

    def __ps(self, img, ps):
        if ps:
            if type(ps) == str:
                return self.RGB颜色选取(img, ps)
            elif type(ps) == tuple or type(ps) == list:
                return self.HSV颜色选取(img, ps)
        return img

    def HSV颜色选取(self, img, HSV颜色范围: tuple):
        lower, upper = HSV颜色范围
        if len(img.shape) != 3:
            print("图像必须是3通道")
            return None
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_red = np.array(lower)
        upper_red = np.array(upper)
        mask = cv2.inRange(img_hsv, lower_red, upper_red)
        img = cv2.bitwise_and(img, img, mask=mask)
        return img

    def RGB颜色选取(self, img, RGB颜色范围: str):
        lower, upper = self.__color_to_range(RGB颜色范围)  # 设置RGB下限和上限
        if lower is None or upper is None:
            return None
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(img, np.array(lower), np.array(upper))
        res = cv2.bitwise_and(img, img, mask=mask)
        img = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)  # 转灰度单通道
        ret, img = cv2.threshold(img, 1, 255, 0)  # 二值化
        return img

    def set_image(self, path):
        self.image_dir = path

    def find_pic2(self,x1, y1, x2, y2, pic_name, delta_color,sim, dir=6):
        max_img = self.captrue(x1, y1, x2, y2)
        min_img = self.obj.imread(self.image_dir + pic_name)

        height1, width1 = max_img.shape[:2]
        height2, width2 = min_img.shape[:2]
        # 获取C数组指针-大图
        max_img = np.asarray(max_img, dtype="uint32")
        max_img = max_img.ctypes.data_as(ctypes.c_char_p)
        # 获取C数组指针-小图
        min_img = np.asarray(min_img, dtype="uint32")
        min_img = min_img.ctypes.data_as(ctypes.c_char_p)
        # 获取C数组指针-偏色
        lower,upper = self.__color_to_range(delta_color,sim)
        lower = np.asarray(lower, dtype="uint32")
        lower = lower.ctypes.data_as(ctypes.c_char_p)
        upper = np.asarray(upper, dtype="uint32")
        upper = upper.ctypes.data_as(ctypes.c_char_p)
        # 获取C数组指针-返回值
        res = np.asarray((0, 0), dtype="int32").ctypes.data_as(ctypes.c_char_p)
        dll.FindPic(max_img, min_img, lower, upper, height1, width1, height2, width2, res)
        if int(res._arr[0]) == -1:
            return False
        else:
            res = res._arr[1] + x1, res._arr[0] + y1
        return list(res)

    def find_pic(self, *args):
        """
        :param img_path: 图片路径
        :param xsd: 相似度
        :return: (x,y) 或者None
        """
        if len(args) == 2:
            img_path, xsd = args
            return self.obj.find_pic(self.ldNum, self.image_dir + img_path, xsd)
        if len(args) == 8:
            if args[7] == 6:
                return self.find_pic2(*args)
            else:
                return self.find_pics(*args)

    def find_pics(self, x1, y1, x2, y2, img_path,delta_color, sim,  method=5):
        img1 = self.captrue(x1, y1, x2, y2)
        img2 = self.obj.imread(self.image_dir + img_path)
        new_img1 = self.__ps(img1, delta_color)
        new_img2 = self.__ps(img2, delta_color)
        # if "点击攻击" in img_path:
        #     cv2.imshow("img1",img1)
        #     cv2.imshow("img2",img2)
        #     cv2.imshow("img3",new_img1)
        #     cv2.imshow("img4",new_img2)
        #     cv2.waitKey()
        result, min_val, max_val, min_loc, max_loc = self.matchTemplate(new_img1, new_img2, method)
        yloc, xloc = np.where(result >= sim)
        if len(xloc):
            return max_loc[0] + x1, max_loc[1] + y1

    def find_picexs(self, x1, y1, x2, y2, img_path, xsd, ps, method=5):
        img1 = self.captrue(x1, y1, x2, y2)
        img2 = self.obj.imread(self.image_dir + img_path)
        new_img1 = self.__ps(img1, ps)
        new_img2 = self.__ps(img2, ps)
        result, min_val, max_val, min_loc, max_loc = self.matchTemplate(new_img1, new_img2, method)
        yloc, xloc = np.where(result >= xsd)
        if len(xloc):
            xloc = [x + x1 for x in xloc]
            yloc = [y + y1 for y in yloc]
            return zip(xloc, yloc)

    @staticmethod
    def matchTemplate(new_img1, new_img2, flag=None):
        if flag is None:
            flag = cv2.TM_CCOEFF_NORMED
        result = cv2.matchTemplate(new_img1, new_img2, flag)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return result, min_val, max_val, min_loc, max_loc

    # 点击,delay表示长按时间
    def left_click(self, x, y, delay=0, interval=1):
        self.obj.touch(self.ldNum, x, y, delay)
        time.sleep(interval)

    # 滑动
    def slide(self, loc1, loc2, delay=0):
        return self.obj.swipe(self.ldNum, loc1, loc2, delay)

    def input(self, str_):
        return self.obj.input_text(self.ldNum, str_)

    def captrue(self, x1, y1, x2, y2):
        self.obj.captrue(self.ldNum)
        img = self.obj.imread(self.image_path)
        img = img[y1:y2, x1:x2]
        return img

    # def find_str(self, x1, y1, x2, y2, xsd, flag="num"):
    #     img = self.captrue(x1, y1, x2, y2)
    #     if flag == "num":
    #         ocr = MID(img, Script_public.TSN.token_dir_path)
    #         return ocr.ocr(xsd)

    def restart_app(self, package_name):
        self.obj.stopapp(self.ldNum, package_name)
        time.sleep(2)
        self.obj.invokeapp(self.ldNum, package_name)

    def __inRange(self, img, lower, upper):
        mask = cv2.inRange(img, np.array(lower), np.array(upper))
        img = cv2.bitwise_and(img, img, mask=mask)
        return img

    def __ps_to_img(self, img, ps):
        """
        :param img: cv图像
        :param ps: 偏色
        :return: 偏色后的cv图像
        """
        # 判断是RGB偏色还是HSV偏色,对应使用遮罩过滤
        if not ps:
            return img

        elif type(ps) == str:
            lower, upper = self.__color_to_range(ps, 1)
            img = self.__inRange(img, lower, upper)

        elif type(ps) == tuple:
            lower, upper = ps
            img_hsv1 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img = self.__inRange(img_hsv1, lower, upper)
        return img

    # 识别数字
    def OcrNum(self, x1, y1, x2, y2, color_format, sim, dirPath):
        """
        :param x1:  x1 整形数:区域的左上X坐标
        :param y1: y1 整形数:区域的左上Y坐标
        :param x2: x2 整形数:区域的右下X坐标
        :param y2: y2 整形数:区域的右下Y坐标
        :param color_format: 字符串:颜色格式串, 可以包含换行分隔符,语法是","后加分割字符串. 具体可以查看下面的示例 .注意，RGB和HSV,以及灰度格式都支持.
        :param sim: 双精度浮点数:相似度,取值范围0.1-1.0
        :param dirPath: 图库路径,用于存储0-9数字模板
        :return: num：字符串数字
        """
        num_dict = {}
        # 遍历图像,并挨个识别
        for i in range(10):
            img_num = dirPath + os.path.sep + f"{i}.bmp"
            locs = self.find_picexs(x1, y1, x2, y2, img_num, sim, color_format)
            if locs:
                for loc in locs:
                    num_dict.update({loc[0]: i})
        # 排序字典
        new_num_list = sorted(num_dict.items(), key=lambda x: x[0])  # 对x轴进行排序

        # 遍历并拼接数字
        nums = "".join([str(new_num[1]) for new_num in new_num_list])
        try:
            return nums
        except:
            return ""


# 识别吞噬币数字
class MID:
    def __init__(self, img, image_dir):
        self.img = img
        self.image_dir = image_dir
        self.num_dict = {}  # 存储 坐标-数字
        self.max_num = 10  # 等做好所有图片，就写10

    def ocr(self, xsd):
        # 定义返回的数据
        num = ""
        # 遍历图像,并挨个识别
        for i in range(self.max_num):
            img = Dnconsole.imread(self.image_dir + f"{i}" + ".bmp")
            self.get_nums(i, img, xsd)
        # 排序字典
        new_num_list = sorted(self.num_dict.items(), key=lambda x: x[0])
        # 取所有识别到的数字，并返数字形式的回字符串
        for item in new_num_list:
            num += str(item[1])
        return num

    # 比对图像
    def get_nums(self, i, img, xsd):
        result, min_val, max_val, min_loc, max_loc = GamePlugIn.matchTemplate(self.img, img, cv2.TM_CCOEFF_NORMED)
        yloc, xloc = np.where(result >= xsd)
        if len(xloc):
            max_locs = list(zip(xloc, yloc))
            for max_loc in max_locs:
                self.num_dict.update({max_loc[0]: i})


def test():
    xsd = 0.95
    path_dir = r"E:\code\python\xiaojia_Timo\Resources\static\tsn\image\token_num\\"
    num = "31"
    path_image = r"E:\code\python\xiaojia_Timo\Resources\static\tsn\image\token_test\%s.bmp" % num
    img = Dnconsole.imread(path_image)
    ocr = MID(img, path_dir)
    return ocr.ocr(xsd)


if __name__ == '__main__':
    print(int(test()))
