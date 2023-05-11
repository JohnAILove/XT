"""
@Time : 2022/8/1 23:07
@Author : 大雄
@Email : 3475228828@qq.com
@func : 配置操作
说明 : 详详情看示例
"""
import configparser


class Config:
    def __init__(self,path):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(path, encoding='gbk')

    # 获取某个标题某个值
    def get_value(self,section,key):
        try:
            return self.config.get(section, key)
        except:
            return ""

    # 获取标题section下所有key=value的(key,value)格式: 返回类似于这种格式[(option1, value1), (option2, value2)]
    def get_items(self,section):
        return self.config.items(section)

    # 添加标题
    def add_section(self,section):
        try:
            self.config.add_section(section)
        except Exception as E:
            pass
            # print("无法添加,可能已有section值 %s"%E)

    # 在标题下写入key-value
    def set(self,section,key,value):
        self.config.set(section,key,value)

    # 保存文件
    def write(self):
        with open(self.path,"w") as fp:
            self.config.write(fp)

    # 邮箱配置示例
    def create_mail(self,user,__pass):
        self.add_section(user)
        self.set(user,"user",user + "@recolte-cn.cn")
        self.set(user, "pass", __pass)
        self.write()

if __name__ == '__main__':
    # 示例
    con = Config("./test.ini") # 初始化
    print(con.add_section("user"))
    # con.create_mail("002","asdfsdf") # 写入
    # print(con.get_items('002'))     # 读取标题下所有key-value
    print(con.get_value('002','user')) # 读取标题下某个key的value