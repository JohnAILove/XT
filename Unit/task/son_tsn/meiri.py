# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/27 1:32
@Auth ： 大雄
@File ：meiri.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import time

from Common.publicFunction import *


class MeiRi:
    def task_fuben(self):
        td_info[self.row_num].progress = "游戏登录"
        max_time = time.time() + self.task_max_time
        while True:
            time.sleep(1)
            progress = td_info[self.row_num].progress
            update_log(f"========={progress}流程=========", self.row_num)
            update_task(self.row_num, progress)

            # 判断是否超时
            if max_time < time.time():
                max_time = get_script_value(gl_info.script, "task_max_time") + time.time()
                update_log(f"任务流程超时{self.task_max_time}s", self.row_num)
                progress = "重启app"
                break

            elif progress == "游戏登录":
                self.gameLogin()
            elif progress == "游戏进入":
                self.gameIn()
            elif progress == "关闭限时优惠广告":
                self.close_GG()
            elif progress == "福利领取":
                self.get_welfare()
            elif progress == "登入公告":
                self.login_GG()
            elif progress == "信件":
                self.mail()
            elif progress == "派遣":
                self.dispatch()
            elif progress == "挖矿":
                self.digging()
            elif progress == "提交吞食币":
                try:
                    self.submit_game_token()
                except Exception as e:
                    update_log("提交吞食币报错,重启app")
                    td_info[self.row_num].progress = "重启app"
            elif progress == "写入数据":
                self.write_csv()

            else:
                break

        return progress

    # 游戏登录
    def gameLogin(self):
        update_log("==============游戏登录================", self.row_num)
        # 初始化循环时间
        max_time = time.time() + self.start_app_delay
        while True:
            time.sleep(2)
            if max_time<time.time():
                update_log(f"游戏登录超时{self.start_app_delay}",self.row_num)
                break
            update_log(f"等待游戏主界面显示 剩余{int(max_time - time.time())}s", self.row_num)
            if self.gp.find_pic(*self.ms["谷歌按钮"]):
                update_log("选择谷歌账号,等待10秒", self.row_num)
                self.gp.left_click(*self.loc["谷歌按钮"])
                time.sleep(10)
                update_log("再次判断画面是否在选择谷歌账号,如果不是则跳转：'游戏进入'", self.row_num)
                if self.gp.find_pic(*self.ms["谷歌按钮"]):
                    continue
                td_info[self.row_num].progress = "游戏进入"
                return
            elif self.gp.find_pic(*self.ms["找不到更新资源"]):
                update_log("找不到更新资源", self.row_num)
                break
            elif self.gp.find_pic(*self.ms["下载更新"]):
                update_log("识别到下载更新,点击确定,并延迟10分钟")
                self.gp.left_click(*self.loc["下载更新确定按钮"])
                self.start_app_delay = self.start_app_delay + self.update_delay
                self.task_max_time = self.task_max_time + self.update_delay
                td_info[self.row_num].progress = "游戏登录"
            elif self.gp.find_pic(*self.ms["雷电商店停止运行"]):
                self.gp.left_click(*self.loc["雷电商店停止运行确定按钮"])
            elif self.gp.find_pic(*self.ms["与server连线中断"]):
                self.gp.left_click(*self.loc["与server连线中断"])
            elif self.gp.find_pic(*self.ms["选择账号"]):
                self.gp.left_click(*self.loc["选择账号第二个"])
            ret = self.gp.find_pic(*self.ms["FTP连接失败确定"])
            if ret: self.gp.left_click(*ret)
        update_log("游戏登录异常，跳转重启游戏", self.row_num)
        td_info[self.row_num].progress = "重启app"

    # 游戏进入
    def gameIn(self):
        update_log("==============游戏进入================", self.row_num)
        # 判断当前界面
        now_dict = {
            "下载更新": self.ms["下载更新"],
            "服务器尚未连接请稍后再试": self.ms["服务器尚未连接请稍后再试"],
            "福利界面": self.ms["福利界面"],
            "关闭限时优惠广告": self.ms["限时优惠"],
            "登入公告": self.ms["登入公告"],
            "福利按钮": self.ms["福利按钮"],
        }
        # 初始化时间
        if self.app_delay_num == app_delay_num:
            self.app_delay_num = time.time() + app_delay_num
        # 判断是否超时卡在点击谷歌界面
        while time.time() < self.app_delay_num:
            time.sleep(2)
            update_log(f"判断是否在游戏进入界面 剩余{int(self.app_delay_num - time.time())}s", self.row_num)
            for k, v in now_dict.items():
                ret = self.gp.find_pic(*v)
                if ret:
                    update_log(k, self.row_num)
                    self.gp.left_click(*ret)
                    if k == "下载更新":
                        update_log("识别到下载更新,点击确定,并延迟10分钟")
                        self.gp.left_click(*self.loc["下载更新确定按钮"])
                        self.start_app_delay = self.start_app_delay + self.update_delay
                        self.task_max_time = self.task_max_time + self.update_delay
                        td_info[self.row_num].progress = "游戏登录"
                    elif k == "服务器尚未连接请稍后再试":
                        td_info[self.row_num].progress = "重启app"
                    else:
                        if k in ["福利界面", "登入公告", "关闭限时优惠广告", "福利按钮"] and gl_info.fuli_state:
                            td_info[self.row_num].progress = "任务完成"
                            return
                        elif k == "福利界面":
                            td_info[self.row_num].progress = "福利领取"
                        elif k == "登入公告":
                            td_info[self.row_num].progress = "登入公告"
                        elif k == "关闭限时优惠广告":
                            td_info[self.row_num].progress = "关闭限时优惠广告"
                        elif k == ["福利按钮"]:
                            update_log("识别到福利按钮,再次等待5秒,福利界面自动弹出", self.row_num)
                            time.sleep(5)
                    return
        update_log("卡在登录界面,重启app", self.row_num)
        td_info[self.row_num].progress = "重启app"

    # 关闭限时优惠广告
    def close_GG(self):
        update_log("==============关闭限时优惠广告================", self.row_num)
        for i in range(10):
            time.sleep(1)
            ret = self.gp.find_pic(*self.ms["限时优惠"])
            if ret:
                self.gp.left_click(*self.loc["关闭限时优惠按钮"])
            elif self.gp.find_pic(*self.ms["福利界面"]):
                td_info[self.row_num].progress = "福利领取"
                return

    # 福利领取
    def get_welfare(self):
        update_log("==============福利领取================", self.row_num)
        for i in range(10):
            time.sleep(1)
            # 查看福利界面是否已打开
            if self.gp.find_pic(*self.ms["福利界面"]):
                update_log("福利界面已打开",self.row_num)
                break
            else:
                fuli_loc = self.gp.find_pic(*self.ms["福利按钮"])
                if fuli_loc:
                    update_log("打开福利界面", self.row_num)
                    self.gp.left_click(*fuli_loc)
                else:
                    update_log("找不到福利按钮",self.row_num)
        else:
            update_log("福利领取异常",self.row_num)
            td_info[self.row_num].progress = "重启app"
            return
        # 点击签到
        ret = self.gp.find_pic(*self.ms["每日签到"])
        if ret:
            update_log("点击每日签到", self.row_num)
            self.gp.left_click(*ret)
            update_log("点击登录好礼", self.row_num)
            for i in range(3):
                update_log("福利上划", self.row_num)
                self.gp.slide(ret, self.loc["福利上滑"])
                time.sleep(1)

            ret = self.gp.find_pic(*self.ms["登入好礼"])
            if ret:
                update_log("点击登入好礼", self.row_num)
                self.gp.left_click(*ret)
                update_log("判断是否可以领取 登入好礼", self.row_num)
                self.login_gift()
        self.welfare_flag = True
        if self.login_flag:
            td_info[self.row_num].progress = "信件"
        else:
            td_info[self.row_num].progress = "登入公告"
            time.sleep(2)

    # 登入公告
    def login_GG(self):
        update_log("==============登入公告================", self.row_num)
        update_log("等待10秒，看是否有公告弹出", self.row_num)
        time.sleep(10)
        for i in range(5):
            time.sleep(1)
            if self.gp.find_pic(*self.ms["登入公告"]) or self.gp.find_pic(*self.ms["今日登入不再提示"]):
                self.gp.left_click(*self.loc["登入公告-关闭按钮"], 0, 2)
                update_log(f"关闭第{i + 1}个登入公告", self.row_num)
            else:
                update_log("登入公告已关闭完", self.row_num)
                break
        self.login_flag = True
        if self.welfare_flag:
            td_info[self.row_num].progress = "信件"
        else:
            td_info[self.row_num].progress = "福利领取"

    # 信件
    def mail(self):
        update_log("==============信件================", self.row_num)
        gift_dict = {
            "退到主界面": (self.gp.find_pic, (*self.ms["谷歌按钮"],)),
            "信件按钮": (self.open_menu, (self.ms["信件按钮"], self.loc["信件按钮"], self.ms["信件界面"])),
            "一键领取": (self.is_pic_and_click, (self.ms["信件界面"], self.loc["信件-一键领取"])),
            "删除空白": (self.is_pic_and_click, (self.ms["信件界面"], self.loc["信件-删除空白"])),
            "关闭信件窗口": (self.is_pic_and_click, (self.ms["信件界面"], self.loc["信件-关闭按钮"])),
        }
        for k, v in gift_dict.items():
            update_log("信件流程:" + k, self.row_num)
            if k == "退到主界面":
                if v[0](*v[1]):
                    update_log(k,self.row_num)
                    td_info[self.row_num].progress = "游戏登录"
                    return False
                else:
                    continue
            if not v[0](*v[1]):
                update_log("信件找图失败", self.row_num)
                # 判断是否有公告界面
                if self.gp.find_pic(*self.ms["今日登入不再提示"]):
                    td_info[self.row_num].progress = "登入公告"
                else:
                    td_info[self.row_num].progress = "重启app"
                return False
        td_info[self.row_num].progress = "派遣"

    # 派遣
    def dispatch(self):
        update_log("==============派遣================", self.row_num)
        # 打开派遣界面
        if self.open_menu(self.ms["派遣按钮"], self.loc["派遣按钮"], self.ms["派遣窗口"]):
            # 选择武将并派遣,花光元宝
            if self.dispatch_son():
                update_log("关闭窗口", self.row_num)
                self.gp.left_click(*self.loc["关闭派遣窗口按钮"])
                td_info[self.row_num].progress = "挖矿"
                return
        else:
            td_info[self.row_num].progress = "重启app"

    # 挖矿
    def digging(self):
        update_log("==============挖矿================", self.row_num)
        if self.open_menu(self.ms["挖矿按钮"], self.loc["挖矿按钮"], self.ms["挖矿界面"]):
            for i in range(4):
                time.sleep(1)
                # 操作两次，确保食物存在
                if not self.is_food(i):
                    if not self.is_food(i):
                        continue
                update_log("已操作两次,确认第{i}旷工无食物", self.row_num)
            update_log("关闭挖矿界面", self.row_num)
            self.gp.left_click(*self.loc["挖矿关闭按钮"])
            td_info[self.row_num].progress = "提交吞食币"
        else:
            td_info[self.row_num].progress = "重启app"

    # 提交吞食币
    def submit_game_token(self):
        if self.open_menu(self.ms["市集按钮"], self.loc["市集按钮"], self.ms["市集-加号"]):
            self.gp.left_click(*self.loc["市集-加号按钮"])
            update_log("已点击加号，判断市集-max按钮是否存在，存在则点击", self.row_num)
            if self.is_pic_click(self.ms["市集-max"], 3):
                self.send_input()
            else:
                time.sleep(2)
                self.gp.left_click(*self.loc["市集-加号按钮"])
                update_log("再次点击加号，判断市集-max按钮是否存在，存在则点击", self.row_num)
                if self.is_pic_click(self.ms["市集-max"], 3):
                    self.send_input()

                else:  # 打不开max界面，说明吞食币为0
                    update_log("点击两次加号都提示无吞食币", self.row_num)
                    self.token = 0
                    self.up_token = 0
                    self.residue_token = 0
            td_info[self.row_num].progress = "写入数据"
        else:
            td_info[self.row_num].progress = "重启app"

    # 写入数据
    def write_csv(self):
        csv = gl_info.csv
        if self.login_now_day > 14:
            self.lgoin_14_flag = True
        update_log(
            f"写入的数据为{self.ldNum, self.login_now_day, self.lgoin_14_flag, self.token, self.up_token, self.residue_token}",
            self.row_num)
        csv.set_key_value(self.ldNum, [self.ldNum, self.login_now_day, self.lgoin_14_flag, self.token, self.up_token,
                                       self.residue_token, "任务完成"])
        td_info[self.row_num].progress = "任务完成"

    def open_menu(self, tz, loc, win_tz):
        if self.is_click_and_pic(tz, self.loc["功能按钮"]):  # 点击功能按钮，直到功能菜单出现
            update_log(f"点击 {tz[0]}", self.row_num)
            self.is_pic_click(tz)  # 等待特征出现，出现就点击
            time.sleep(2)
            if self.gp.find_pic(*win_tz):  # 出现窗口界面，就退出
                return True
        return False

    def login_gift(self):
        for i in range(5):
            # 点击领取
            if self.gp.find_pic(*self.ms["登入好礼-领取"]):
                update_log("登入好礼 领取", self.row_num)
                self.gp.left_click(*self.loc["登入好礼-领取"])
            else:
                update_log("今日已领取过，无法再次领取", self.row_num)
                break
        # 获取当前天数
        self.login_now_day = self.get_now_day()
        if self.login_now_day <= self.login_gift_max_num:
            update_log("关闭福利界面", self.row_num)
            self.gp.left_click(*self.loc["福利界面-关闭按钮"])
            return True

    # 找到界面，就点击
    def is_pic_and_click(self, tz, loc):
        for i in range(10):
            time.sleep(1)
            if self.gp.find_pic(*tz):
                self.gp.left_click(*loc)
                return True
        td_info[self.row_num].progress = "任务异常"
        return False

    # 点击直到界面出现
    def is_click_and_pic(self, tz, loc):
        for i in range(10):
            time.sleep(1)
            if self.gp.find_pic(*tz):
                return True
            else:
                update_log(f"点击{loc}", self.row_num)
                self.gp.left_click(*loc)
        td_info[self.row_num].progress = "任务异常"
        return False

    # 找到界面,并点击该位置
    def is_pic_click(self, tz, num=10):
        for i in range(num):
            time.sleep(1)
            ret = self.gp.find_pic(*tz)
            if ret:
                self.gp.left_click(*ret)
                return True
        return False

    # 派遣武将
    def dispatch_son(self):
        update_log("==============派遣武将================", self.row_num)
        dispatch_dict = {
            "请选择武将": self.ms["请选择武将"],
            "确定武将": self.ms["确定武将"],
            "出发": self.ms["出发"],
            "快速完成": self.ms["快速完成"],  # 前三次可以快速完成，超过后，自动跳过,通过__send函数领取
            "派遣武将-领取": self.ms["派遣武将-领取"],
            "闪退桌面": self.desktop(),
            "闪退主界面":self.ms["谷歌按钮"]
        }
        max_time = self.paiqian_task_max_time + time.time()
        chufa_count = 0
        while True:
            time.sleep(1)
            if max_time < time.time():
                update_log("派遣武将超时,重启app", self.row_num)
                return False
            for k, v in dispatch_dict.items():
                if k == "闪退桌面" and self.desktop():
                    update_log(k, self.row_num)
                    update_log("模拟器闪退到桌面,重新启动app", self.row_num)
                    td_info[self.row_num].progress = "重启app"
                    return False
                elif k != "闪退桌面":
                    ret = self.gp.find_pic(*v)
                    if ret:
                        update_log(k, self.row_num)
                        if k == "闪退主界面":
                            update_log(k, self.row_num)
                            td_info[self.row_num].progress = "游戏登录"
                            return False
                        self.gp.left_click(*ret)
                        # 判断是否满足9次
                        if k == "出发":
                            chufa_count += 1
                            if self.gp.find_pic(*v):
                                update_log("已到达9次,排遣完成", self.row_num)
                                return True
                            if chufa_count >= 9:
                                update_log("次数累计9次，派遣完成",self.row_num)
                                return True
                    else:
                        time.sleep(0.1)
            if self.send() == "元宝不足":
                update_log("元宝不足", self.row_num)
                return True

    # 排遣武将-花费元宝购买
    def send(self):
        ret = self.gp.find_pic(*self.ms["花费元宝购买-是"])
        if ret:
            update_log("点击 购买元宝 是 并等待3秒", self.row_num)
            self.gp.left_click(*ret, 0, 2)
            if self.gp.find_pic(*self.ms["出发"]):
                return "元宝不足"
            # 如果碰到快速完成，则判断点击快速完成后，是否还有快速完成
            ret = self.gp.find_pic(*self.ms["快速完成"])
            if ret:
                self.gp.left_click(*ret, 0, 2)
                ret = self.gp.find_pic(*self.ms["花费元宝购买-是"])
                if ret:
                    update_log("点击 购买元宝 是 并等待2秒", self.row_num)
                    self.gp.left_click(*ret, 0, 2)
                    ret = self.gp.find_pic(*self.ms["快速完成"])
                    if ret:
                        return "元宝不足"

    # 获取当前天数
    def get_now_day(self):
        update_log("获取当前天数", self.row_num)
        if self.gp.find_pic(*self.ms["全部完成"]):
            update_log("已全部完成", self.row_num)
            new_day = 15
            return new_day
        for delay, tz_num in enumerate(self.ms["天数列表"]):
            if self.gp.find_pic(*self.ms["天数范围"], *tz_num):
                new_day = delay + 1
                break
        else:
            update_log("无法识别当前天数,沿用旧的天数", self.row_num)
            new_day = self.login_now_day
        update_log(f"当前天数为 {new_day}", self.row_num)
        return new_day

    # 喂食判定
    def is_food(self, i):
        update_log(f"点击喂食 第{i}个旷工", self.row_num)
        self.gp.left_click(*self.loc["喂食"][i])
        max_loc = self.gp.find_pic(*self.ms["喂食-max"])
        if max_loc:
            update_log("输入喂食数量max", self.row_num)
            self.gp.left_click(*max_loc)
            update_log("确认喂食", self.row_num)
            self.gp.left_click(*self.loc["喂食-确定"])
            return True

    # 获取吞食币
    def get_token(self):
        for i in range(10):
            time.sleep(1)
            update_log(f"第{i}次尝试获取吞食币", self.row_num)
            num = self.gp.OcrNum(*self.ms["市集-存入吞食币范围"])
            if num:
                num = int(num)
                update_log("已获取到吞噬币", self.row_num)
                break
        else:
            update_log("未获取到吞噬币,请检测脚本", self.row_num)
            raise "未获取到吞噬币,请检测脚本"
        update_log(f"当前吞食币为 {num}", self.row_num)
        return num

    # 输入吞食币个数
    def input(self, num):
        if num == "max":
            self.gp.left_click(*self.loc["吞食币MAX"])
        else:
            # 先点击min才能输入币
            self.gp.left_click(*self.loc["吞食币MIN"])
            self.gp.left_click(*self.loc["吞食币数量位置"])
            self.gp.input(num)
        self.gp.left_click(*self.loc["市集-存入-确定"])
        self.gp.left_click(*self.loc["市集-存入-确定"])
        for i in range(5):
            self.gp.left_click(*self.loc["市集-存入-发送至交易市场"])
            time.sleep(2)
            if self.gp.find_pic(*self.ms["转移成功"]):
                update_log("转移成功", self.row_num)
                self.gp.left_click(*self.loc["转移或处理中的确定"])
                return True
            elif self.gp.find_pic(*self.ms["资料处理中"]):
                update_log("资料处理中", self.row_num)
            elif self.gp.find_pic(*self.ms["上传失败"]):
                update_log("上传失败", self.row_num)
            else:
                update_log("找不到图，可能卡，再次等待", self.row_num)
                time.sleep(2)
            self.gp.left_click(*self.loc["转移或处理中的确定"])

        update_log("尝试5次，都无法上传成功，本次上传吞食币失败", self.row_num)

    # 获取csv中的某个单元格内容
    def get_csv_column(self, column):
        line = gl_info.csv.get_value(self.ldNum)
        if line is None:
            raise "获取csv有误"
        if type(line[column]) != str:
            line[column] = str(line[column])
        return line[column]

    # 输入并上传吞食币
    def send_input(self):
        num = self.get_token()
        update_log(f"当前吞食币为 {num}", self.row_num)
        if num and self.login_now_day >= 15:
            update_log("最后一天,提交所有吞食币", self.row_num)
            if self.input("max"):
                self.residue_token = 0
            else:
                self.residue_token = num

        elif num and num >= self.max_token:
            update_log(f"提交 {self.max_token}个吞食币", self.row_num)
            if self.input(self.max_token):
                self.residue_token = num - self.max_token
            else:
                self.residue_token = num
        else:
            update_log(f"小于{self.max_token}个,且不是最后一天,不提交吞食币", self.row_num)
            self.residue_token = num
        self.up_token = self.up_token + (num - self.residue_token)  # 原先的上传数量+ 本次的上传数量 = 历史上传交易数量
        self.token = self.up_token + self.residue_token  # 原先的上传数量 + 本次剩余的数量 = 吞食币数量总和
        update_log(f"吞食币数量{self.token}", self.row_num)
        update_log(f"已上传交易市集{self.up_token}", self.row_num)
        update_log(f"剩余吞食币为{self.residue_token}", self.row_num)

    # 判断是否闪退到桌面
    def desktop(self):
        return desktop_name == gl_info.ld.get_activity_name(self.ldNum)
