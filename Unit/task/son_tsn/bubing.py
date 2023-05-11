# -*- coding: utf-8 -*-
"""
@Time ： 2023/2/27 1:32
@Auth ： 大雄
@File ：bubing.py
@IDE ：PyCharm
@Email:3475228828@qq.com
@func:功能
"""
import random

from Common.publicFunction import *


class BuBing:
    def bubing(self):
        td_info[self.row_num].progress = "补兵登录"
        max_time = time.time() + self.bubing_task_time
        while True:
            time.sleep(1)
            progress = td_info[self.row_num].progress
            update_log(f"当前流程:{progress}", self.row_num)
            update_task(self.row_num, progress)
            # 判断是否超时
            if max_time < time.time():
                update_log(f"补兵任务流程超时{self.bubing_task_time}s",self.row_num)
                progress = "重启app"
                break
            elif progress == "补兵登录":
                self.bubing_login()
            elif progress == "主界面判定":
                self.bubing_zhujiemian()
            elif progress == "福利领取":
                self.get_welfare()
                if td_info[self.row_num].progress == "重启app":
                    td_info[self.row_num].progress = "补兵登录"
            elif progress == "关闭限时优惠广告":
                self.close_GG()
                if td_info[self.row_num].progress != "福利领取":
                    td_info[self.row_num].progress = "主界面判定"
            elif progress == "登入公告":
                self.login_GG()
            elif progress == "任务流程":
                self.bubing_task()
                if td_info[self.row_num].progress == "任务流程":
                    td_info[self.row_num].progress = "重启app"
            elif progress == "创建角色":
                self.create_route()
            elif progress == "属性选择界面":
                self.shuxing_check()
            elif progress == "信件":
                # 先判断是否已经领取过福利,如果没领取过，需要再次领取
                if not self.welfare_flag:
                    update_log("未领取福利，先领取福利在打开信件",self.row_num)
                    td_info[self.row_num].progress = "福利领取"
                    continue
                else:
                    update_log("开始执行信件流程",self.row_num)
                    self.mail()
                if td_info[self.row_num].progress == "登入公告":
                    continue
                elif td_info[self.row_num].progress == "重启app":
                    continue
                elif td_info[self.row_num].progress == "游戏登录":
                    td_info[self.row_num].progress == "补兵登录"
                    continue
                elif td_info[self.row_num].progress == "派遣":
                    if self.bubing_task_flag:
                        td_info[self.row_num].progress = "清理背包"
                    else:
                        td_info[self.row_num].progress = "补兵登录"
                else:
                    raise "信件流程执行完后无法判断下一步流程，导致错误"
            elif progress == "清理背包":
                self.beibao()
                td_info[self.row_num].progress = "派遣"
            elif progress == "派遣":
                # 派遣之前，先检查任务是否已完成，武将是否已存入，如果是在进行派遣
                if self.bubing_task_flag:
                    self.dispatch()
                    if td_info[self.row_num].progress == "挖矿":
                        td_info[self.row_num].progress = "任务完成"
                        continue
                    if td_info[self.row_num].progress == "游戏登录":
                        td_info[self.row_num].progress == "补兵登录"
                        continue
                if td_info[self.row_num].progress == "派遣":
                    td_info[self.row_num].progress == "主界面判定"
            elif progress == "重启app":
                if self.desktop():
                    update_log("意外闪退到桌面，重启app",self.row_num)
                    break
                else:
                    update_log("其他原因重启app",self.row_num)
                    break
            else:
                break
        return progress

    # 补兵登录
    def bubing_login(self):
        update_log("==============补兵登录================", self.row_num)
        tz = {
            "谷歌按钮": self.ms["谷歌按钮"],
            "创建角色界面": self.ms["创建角色界面"],
            "属性选择界面": self.ms["属性选择界面"],
            "HPSPEXP": self.ms["HPSPEXP"],
        }
        tz2 = {
            "下载更新": self.ms["下载更新"],
            "游戏账号登录": self.ms["游戏账号登录"],
            "创建玩家资料": self.ms["创建玩家资料"],
            "使用谷歌账号登录": self.ms["使用谷歌账号登录"],
            "雷电商店停止运行": self.ms["雷电商店停止运行"],
            "FTP连接失败确定": self.ms["FTP连接失败确定"],
            "与server连线中断": self.ms["与server连线中断"],
            "选择账号": self.ms["选择账号"],
        }
        max_time = time.time() + self.start_app_delay
        while True:
            time.sleep(2)
            if max_time< time.time():
                update_log(f"补兵任务流程超时{self.start_app_delay}s", self.row_num)
                td_info[self.row_num].progress = "重启app"
                break
            for k, v in tz.items():
                ret = self.gp.find_pic(*v)
                if ret:
                    progress = k
                    update_log(f"当前界面:{progress}", self.row_num)
                    break
            else:
                progress = "未知界面"
            if progress == "谷歌按钮":
                update_log("点击谷歌按钮",self.row_num)
                self.gp.left_click(*self.loc["谷歌按钮"],interval=10)
            elif progress == "创建角色界面":
                td_info[self.row_num].progress = "创建角色"
                break
            elif progress == "属性选择界面":
                td_info[self.row_num].progress = "属性选择界面"
                break
            elif progress == "HPSPEXP":
                td_info[self.row_num].progress = "主界面判定"
                break
            elif progress == "未知界面":
                self.bubing_login_weizhi(tz2)
            if td_info[self.row_num].progress == "重启app":
                break

    # 补兵登录未知界面
    def bubing_login_weizhi(self, tz2):
        update_log("补兵登录未知界面流程",self.row_num)
        for k, v in tz2.items():
            ret = self.gp.find_pic(*v)
            if ret:
                progress = k
                update_log(f"补兵登录未知界面当前界面:{progress}", self.row_num)
                break
        else:
            progress = "未知界面"
        if progress == "下载更新":
            self.down_update()
        elif progress == "游戏账号登录":
            update_log("点击继续，并等待10秒", self.row_num)
            self.gp.left_click(*self.loc["以xx身份继续"], interval=2)
            self.gp.left_click(*self.loc["以xx身份继续"], interval=10)

        elif progress == "创建玩家资料":
            self.gp.left_click(*self.loc["创建玩家资料-创建"])
            self.gp.left_click(*self.loc["创建玩家资料-创建"])
            time.sleep(5)
        elif progress == "使用谷歌账号登录":
            self.google_login()
        elif progress == "雷电商店停止运行":
            self.gp.left_click(*self.loc["雷电商店停止运行确定按钮"])
        elif progress == "FTP连接失败确定":
            if ret:
                self.gp.left_click(*ret)
            td_info[self.row_num].progress = "重启app"
        elif progress == "与server连线中断":
            self.gp.left_click(*self.loc["与server连线中断"])
            td_info[self.row_num].progress = "重启app"
        elif progress == "选择账号":
            if ret:
                self.gp.left_click(self.loc["选择账号上一个"][0]+ret[0],self.loc["选择账号上一个"][1]+ret[1], interval=10)
        else:
            update_log("等到2秒",self.row_num)
            time.sleep(2)

    # 判断当前界面是任务界面，还是重启进入后，需要关闭福利
    def bubing_zhujiemian(self):
        update_log("===============主界面判定===============", self.row_num)
        tz = {
            "福利界面": self.ms["福利界面"],
            "关闭限时优惠广告": self.ms["限时优惠"],
            "登入公告": self.ms["登入公告"],
            "HPSPEXP2": self.ms["HPSPEXP2"],
            "HPSPEXP3": self.ms["HPSPEXP3"],
            "HPSPEXP4": self.ms["HPSPEXP4"],
            "下一步": self.ms["下一步"],
            "空白页": self.ms["空白页"],
            "属性选择界面": self.ms["属性选择界面"],
            "重复登入断线-是":self.ms["重复登入断线-是"],
        }
        time.sleep(2)
        for k, v in tz.items():
            ret = self.gp.find_pic(*v)
            print(v, "====", ret)
            if ret:
                progress = k
                update_log(f"主界面判定当前界面:{progress}", self.row_num)
                break
        else:
            progress = "未知界面"
        if progress == "福利界面":
            td_info[self.row_num].progress = "福利领取"
        elif progress == "关闭限时优惠广告":
            td_info[self.row_num].progress = "关闭限时优惠广告"
        elif progress == "登入公告":
            td_info[self.row_num].progress = "登入公告"
        elif progress in ["HPSPEXP2", "HPSPEXP3", "HPSPEXP4", "空白页", "下一步"]:
            td_info[self.row_num].progress = "任务流程"
        elif progress == "属性选择界面":
            td_info[self.row_num].progress = "属性选择界面"
        elif progress == "重复登入断线-是":
            td_info[self.row_num].progress = "任务流程"
        elif progress == "未知界面":
            update_log("等待2秒",self.row_num)
            time.sleep(2)

    # 下载更新
    def down_update(self):
        update_log("识别到下载更新,点击确定,并延迟10分钟",self.row_num)
        self.gp.left_click(*self.loc["下载更新确定按钮"])
        self.start_app_delay = self.start_app_delay + self.update_delay
        self.task_max_time = self.task_max_time + self.update_delay
        td_info[self.row_num].progress = "补兵登录"

    # 使用谷歌账号登录
    def google_login(self):
        time.sleep(1)
        self.gp.slide(*self.loc["使用谷歌账号登录下滑"])
        time.sleep(1)
        self.gp.slide(*self.loc["使用谷歌账号登录下滑"])
        time.sleep(1)
        self.gp.slide(*self.loc["使用谷歌账号登录下滑"])
        time.sleep(1)
        self.gp.left_click(*self.loc["使用谷歌账号登录-继续"])
        time.sleep(10)

    # 创建角色
    def create_route(self):
        update_log("===============创建角色===============", self.row_num)
        # 随机点几次造型
        for i in range(random.randint(1, 4)):
            self.gp.left_click(*self.loc["随机造型"])
        self.gp.left_click(*self.loc["创建角色-下一步"], interval=2)
        if self.gp.find_pic(*self.ms["属性选择界面"]):
            td_info[self.row_num].progress = "属性选择界面"

    #   属性选择
    def shuxing_check(self):
        update_log("===============属性选择===============", self.row_num)
        # 选择属性
        for i in range(10):
            if self.gp.find_pic(*self.ms["攻击6次"]):
                break
            else:
                self.gp.left_click(*self.loc["攻击加号"])
                self.gp.left_click(*self.loc["攻击加号"])
        for i in range(10):
            # 随机名称
            self.gp.left_click(*self.loc["随机名称"])
            self.gp.left_click(*self.loc["创建角色-下一步"])
            time.sleep(1)
            if self.gp.find_pic(*self.ms["任务自宅-下一步"]):
                break
        td_info[self.row_num].progress = "主界面判定"

    # 任务流程
    def bubing_task(self):
        update_log("===============任务流程===============", self.row_num)
        tz = {
            "任务自宅-下一步": self.ms["任务自宅-下一步"],
            "空白页": self.ms["空白页"],
            "可切换对话目标": self.ms["可切换对话目标"],
            "开启任务列表": self.ms["开启任务列表"],
            "吞噬奇遇-前往": self.ms["吞噬奇遇-前往"],
            "豚郡普户": self.ms["豚郡普户"],
            "豚郡街道": self.ms["豚郡街道"],
            "豚郡城门": self.ms["豚郡城门"],
            "豚郡客栈": self.ms["豚郡客栈"],
        }
        tz2 = {
            "下一步": self.ms["下一步"],
            "头盔带好": self.ms["头盔带好"],
            "关闭背包": self.ms["关闭背包"],
            "头盔带好2": self.ms["头盔带好2"],
            "穿上装备": self.ms["穿上装备"],
            "点击攻击": self.ms["点击攻击"],
            "选择攻击对象": self.ms["选择攻击对象"],
            "开启状态": self.ms["开启状态"],
            "完成确定分配点数": self.ms["完成确定分配点数"],
            "我已经准备好了": self.ms["我已经准备好了"],

            "回复型水系": self.ms["回复型水系"],
            "点选功能钮": self.ms["点选功能钮"],
            "选择队伍": self.ms["选择队伍"],
            "出战": self.ms["出战"],
            "出战2": self.ms["出战2"],
            "离开此处-要": self.ms["离开此处-要"],
            "谷歌按钮": self.ms["谷歌按钮"],
            "窗口x": self.ms["窗口x"],
            "关闭队伍": self.ms["关闭队伍"],
        }
        max_time = time.time() + self.bubing_task_time
        while True:
            time.sleep(1)
            if max_time<time.time():
                update_log(f"任务流程超时{self.bubing_task_time}s", self.row_num)
                break
            for k, v in tz.items():
                ret = self.gp.find_pic(*v)
                print(v, ret)
                if ret:
                    progress = k
                    update_log(f"任务流程当前界面 {progress}", self.row_num)
                    break
            else:
                progress = "未知界面"

            if progress == "空白页":
                if ret:
                    ret2 = self.gp.find_pic(*self.ms["回复型水系"])
                    ret3 = self.gp.find_pic(*self.ms["头盔带好"])
                    ret4 = self.gp.find_pic(*self.ms["重复登入断线-是"])
                    if ret2:
                        update_log("选择回复系水系", self.row_num)
                        self.gp.left_click(*ret2)
                    elif ret3:
                        self.bubing_toukui()
                        update_log("装备头盔流程", self.row_num)
                        self.gp.left_click(*ret3)
                    elif ret4:
                        update_log("重复登入掉线-点击是", self.row_num)
                        self.gp.left_click(*ret4)
                    else:
                        update_log("点击空白页", self.row_num)
                        self.gp.left_click(*ret)

            elif progress in ["任务自宅-下一步", "头盔带好2"]:
                if ret:
                    update_log(f"点击{progress}", self.row_num)
                    self.gp.left_click(*ret)
            elif progress == "吞噬奇遇-前往":
                self.gp.left_click(*self.loc["吞噬奇遇-前往"])
                self.gp.left_click(*self.loc["吞噬奇遇-前往2"])
            elif progress in ["可切换对话目标"]:
                update_log("点击功能按钮", self.row_num)
                self.is_pic_and_click(tz[progress], self.loc["切换对话目标"])
            elif progress == "开启任务列表":
                update_log("开启任务列表", self.row_num)
                self.is_pic_and_click(tz[progress], self.loc["任务"])
            elif progress == "豚郡普户":
                self.tunjunpuhu()
            elif progress == "豚郡街道":
                if self.bubing_zhuxian_flag:
                    self.tunjunjiedao()
                else:
                    self.gp.left_click(*self.loc["主线任务"])
            elif progress == "豚郡城门":
                if self.bubing_zhuxian_flag:
                    self.tunjunchengmen()
                else:
                    self.gp.left_click(*self.loc["主线任务"])
            elif progress == "豚郡客栈":
                if self.tunjunkezhan():
                    break  # 退出任务流程
            elif progress == "未知界面":
                for k, v in tz2.items():
                    ret = self.gp.find_pic(*v)
                    print(v, ret)
                    if ret:
                        progress = k
                        update_log(f"任务流程未知界面当前界面:{progress}", self.row_num)
                        break
                else:
                    progress = "未知界面"
                if progress == "完成确定分配点数":
                    self.gp.left_click(*self.loc["重置点数-确定"])
                    self.gp.left_click(*self.loc["重置点数-最后一次"])
                    self.gp.left_click(*self.loc["状态-关闭"])
                elif progress == "穿上装备":
                    if ret:
                        self.gp.left_click(ret[0] + self.loc["穿上装备偏移"][0], ret[1] + self.loc["穿上装备偏移"][1])

                elif progress == "点击攻击":
                    self.gp.left_click(*self.loc["点击攻击"])
                    self.gp.left_click(*self.loc["选择攻击对象"])

                elif progress == "选择攻击对象":
                    self.gp.left_click(*self.loc["选择攻击对象"])

                elif progress == "开启状态":
                    self.gp.left_click(*self.loc["状态按钮"])
                elif progress == "我已经准备好了":
                    self.gp.left_click(*self.loc["我已经准备好了"])
                    if not self.wangluobadouyao():
                        break

                elif progress in ["回复型水系", "出战", "出战2", "离开此处-要", "头盔带好2", "关闭背包", "关闭队伍",
                                 "下一步"]:
                    ret = self.gp.find_pic(*self.ms[k])
                    if ret:
                        self.gp.left_click(*ret)
                    if k == "离开此处-要":
                        time.sleep(10)

                elif progress == "点选功能钮":
                    self.gp.left_click(*self.loc["功能按钮"])
                    self.gp.left_click(*self.loc["队伍"])

                elif progress == "选择队伍":
                    if ret:
                        self.gp.left_click(ret[0] + self.loc["选择队伍偏移"][0], ret[1] + self.loc["选择队伍偏移"][1])

                elif progress == "谷歌按钮":
                    td_info[self.row_num].progress = "补兵登录"
                    break
                elif progress == "窗口x":
                    if self.gp.find_pic(*self.ms["重置点数"]):
                        self.gp.left_click(*self.loc["重置点数"])
                        self.gp.left_click(*self.loc["增加属性"])
                        self.gp.left_click(*self.loc["重置点数-确定"])
                        self.gp.left_click(*self.loc["重置点数-最后一次"])
                    self.gp.left_click(*self.loc["状态-关闭"])
                elif progress == "头盔带好":
                    self.bubing_toukui()
                else:
                    if self.bubing_zhuxian_flag:
                        update_log("已做过简雍家任务,等待2秒", self.row_num)
                    elif self.desktop():
                        update_log("意外闪退到桌面，重启app",self.row_num)
                        td_info[self.row_num].progress = "重启app"
                        return
                    else:
                        update_log("点击主线任务",self.row_num)
                        self.gp.left_click(*self.loc["主线任务"])
                    time.sleep(2)

    def tunjunpuhu(self):
        update_log("豚郡普户", self.row_num)
        tz = {
            "空白页": self.ms["空白页"],
            "没想去不想回答": self.ms["没想去不想回答"],

        }
        count = 0
        for i in range(10):
            for k, v in tz.items():
                ret = self.gp.find_pic(*v)
                if ret:
                    progress = k
                    update_log(f"豚郡普户:{progress}", self.row_num)
                    break
            else:
                progress = "未知界面"
            if progress in ["空白页", "没想去不想回答"]:
                if ret:
                    self.gp.left_click(*ret)
                if progress == "空白页" and count:
                    self.gp.left_click(*self.loc["关闭世界弹窗1"])
                    self.gp.left_click(*self.loc["关闭世界弹窗2"])
                    break
                if progress == "没想去不想回答":
                    count += 1
            if progress == "未知界面":
                update_log("点击主线任务",self.row_num)
                self.gp.left_click(*self.loc["主线任务"])
        self.bubing_zhuxian_flag = True
        for i in range(5):
            ret = self.gp.find_pic(*self.ms["走出豚郡"])
            if ret:
                update_log("准备走出豚郡", self.row_num)
                self.gp.left_click(*ret, interval=3)
        update_log("前往豚郡城门", self.row_num)

    def tunjunjiedao(self):
        update_log("当前在豚郡街道,准备前往豚郡城门",self.row_num)
        self.gp.left_click(*self.loc["前往豚郡城门"], interval=3)

    def tunjunchengmen(self):
        update_log("已到豚郡城门", self.row_num)
        self.gp.left_click(*self.loc["豚郡客栈"], interval=3)

    def tunjunkezhan(self):
        update_log("已到豚郡客站=============", self.row_num)
        max_time = time.time() + self.dianxiaoer_time
        self.bubing_task_flag = True
        update_log("点击店小二", self.row_num)
        self.gp.left_click(*self.loc["店小二"], interval=2)
        while True:
            time.sleep(1)
            if max_time < time.time():
                update_log("豚郡客站超时",self.row_num)
                td_info[self.row_num].progress = "重启app"
                return True
            if self.gp.find_pic(*self.ms["登入公告"]):
                td_info[self.row_num].progress = "登入公告"
                return True

            ret = self.gp.find_pic(*self.ms["武将"])
            if ret:
                update_log("点击武将", self.row_num)
                self.gp.left_click(*ret)
            else:
                for i in range(10):
                    update_log("选择店小二", self.row_num)
                    if self.gp.find_pic(*self.ms["店小二"]):
                        self.gp.left_click(*self.loc["对话"], interval=2)
                        break
                    else:
                        self.gp.left_click(*self.loc["切换对话目标"])
            ret = self.gp.find_pic(*self.ms["武将"])
            if ret:
                update_log("点击武将", self.row_num)
                self.gp.left_click(*ret, interval=2)
            if self.gp.find_pic(*self.ms["客栈"]):
                cunru = self.gp.find_pic(*self.ms["存入"])
                if cunru:
                    update_log("存入武将", self.row_num)
                    self.gp.left_click(*cunru, interval=2)
                ret = self.gp.find_pic(*self.ms["窗口x"])
                if ret:
                    update_log("关闭客栈窗口", self.row_num)
                    self.gp.left_click(*ret, interval=2)
                    td_info[self.row_num].progress = "信件"
                    return True

    def beibao(self):
        update_log("背包流程", self.row_num)
        tz = {
            "打开背包": self.ms["背包"],
            "宝箱使用": self.ms["宝箱使用"],
            "10000赞宝箱": self.ms["10000赞宝箱"],
            "5000赞宝箱": self.ms["5000赞宝箱"],
            "2500赞宝箱": self.ms["2500赞宝箱"],
            "开服礼包宝箱": self.ms["开服礼包宝箱"],
            "已打开背包界面": self.ms["已打开背包界面"],
        }
        tz_key = list(tz.keys())
        count = 0
        for i in range(20):
            for k, v in tz.items():
                ret = self.gp.find_pic(*v)
                if ret:
                    progress = k
                    update_log(f"当前界面 {progress},计数{count}", self.row_num)
                    break
            else:
                progress = "背包：未知界面"
            if progress in tz_key[:-1]:
                if ret: self.gp.left_click(*ret)
            elif progress == tz_key[-1]:
                count += 1
                if count >= 5:
                    break
        update_log("点击状态窗口x",self.row_num)
        self.gp.left_click(*self.loc["状态窗口关闭x"])

    # 装备头盔
    def bubing_toukui(self):
        update_log("装备头盔流程，主备点击：背包，头盔未知，装备按钮，关闭",self.row_num)
        self.gp.left_click(500, 500)
        self.gp.left_click(*self.loc["背包"], interval=2)
        self.gp.left_click(*self.loc["头盔-背包位置"], interval=2)
        self.gp.left_click(*self.loc["头盔-装备按钮"], interval=2)
        self.gp.left_click(*self.loc["状态-关闭"], interval=2)

    # 网络巴豆妖
    def wangluobadouyao(self):
        max_time = time.time() + 60*2
        gongji_flag = False
        tz = {
            "攻击巴豆妖": self.ms["攻击巴豆妖"],
            "网罗巴豆妖": self.ms["网罗巴豆妖"],
            "选择网罗": self.ms["选择网罗"],
            "半血巴豆妖": self.ms["半血巴豆妖"],
            "满血巴豆妖": self.ms["满血巴豆妖"],
            "选择攻击指令": self.ms["选择攻击指令"],
        }
        while True:
            time.sleep(1)
            if max_time < time.time():
                update_log("网络巴豆妖超时",self.row_num)
                td_info[self.row_num].progress = "重启app"
                return False
            for k,v in tz.items():
                ret = self.gp.find_pic(*v)
                if ret:
                    progress = k
                    update_log("网罗巴豆妖界面:" + progress,self.row_num)
                    break

            # if progress == "选择攻击指令":
            #     self.gp.left_click(*self.loc["点击攻击"])
            #     self.gp.left_click(*self.loc["攻击巴豆妖"])
            #     self.gp.left_click(*self.loc["选择网罗"])
            #     self.gp.left_click(*self.loc["网罗巴豆妖"])

            if progress == "攻击巴豆妖":
                if ret:
                    self.gp.left_click(ret[0] + self.loc["攻击偏移"][0], ret[1] + self.loc["攻击偏移"][1],interval=2)

            elif progress == "选择网罗":
                if ret:
                    self.gp.left_click(ret[0] + self.loc["选择网罗偏移"][0], ret[1] + self.loc["选择网罗偏移"][1],interval=2)
            elif progress == "网罗巴豆妖":
                self.gp.left_click(ret[0] + self.loc["选择网罗偏移"][0], ret[1] + self.loc["选择网罗偏移"][1], interval=2)
                return True

            elif progress == "满血巴豆妖" and not gongji_flag:
                self.gp.left_click(*self.loc["攻击"],interval=2)
                self.gp.left_click(*self.loc["攻击巴豆妖"],interval=2)
                if not self.gp.find_pic(*self.ms[progress]):
                    update_log("已攻击巴豆妖",self.row_num)
                    gongji_flag = True
            else:
                if gongji_flag:
                    update_log("已攻击过巴豆妖，此次网络巴豆妖",self.row_num)
                    self.gp.left_click(*self.loc["网罗按钮"])
                    self.gp.left_click(*self.loc["巴豆妖位置"])
                    return True
                time.sleep(2)
                update_log("等待2秒",self.row_num)

