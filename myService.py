# -*- coding:utf-8 -*-
import sys


class Service:
    # 每次个建立的连接，都有一个相应的service实例对应
    __data_location = ""
    __user_list = {}
    __cmd_dict = {'$login': 1,
                  '$signup': 2,
                  '$logout': 3}

    def __init__(self, conn):
        self.connection = conn
        self.username = ""
        self.stat = 0           # 表示用户当前所处状态，0表示未登录，1表示已登录

    def welcome_program(self, ):
        print ('Connected by', self.connection.getpeername())
        info = "Welcome!\nYou could log in, or sign up a new account"
        self.connection.sendall(info)
     #   while True:     # 停止条件待定
        ret = self.__service_program(self.connection)
        self.connection.sendall(ret)

    def __service_program(self, conn, stat=0):
        # stat表示用户当前所处状态，0表示未登录，1表示已登录
        # data = recv() 接受客户端请求
        data = conn.recv(1024)
        # 处理请求
        cmd = Service.__parse_data(data)
        if cmd[0] > 2:
            return "You must log in first"
        if cmd[0] == 1:
            return self.login(cmd)

    def login(self, cmd):
        if self.stat is 0:
            if Service.__check_login(cmd[1], cmd[2]):
                self.stat = 1                   # 修改登录状态
                return "log in successful"
            else:
                return "wrong password or account"
        else:
            return "You have already logged in"

    def __logout(self):
        if self.stat is 0:
            return "You haven't logged in yet."
        if self.stat is 1:
            # 停止记录时间并保存到本地
            self.stat = 0           # 修改登录状态
            return "logout successful"

    @staticmethod
    def __check_login(account, pwd):
        if account in Service.__user_list:  # 账号存在时验证密码
            return Service.__user_list[account].password == pwd
        return False

    @staticmethod
    def __parse_data(str):
        # 将接受到的字符串处理成[cmd_no, args...]的形式，cmd_no表示指令编号
        cmd = str.split()
        if cmd.__len__() <= 0:
            raise ValueError("invalid command length")
        if cmd[0][0] != '$':        # 判断第一个字符是否是$
            raise ValueError("invalid command")
        cmd[0] = Service.__cmd_dict[cmd[0]]
        return cmd


def fun(conn):
    s = Service(conn)
    s.welcome_program()

if __name__ == "__main__":
    # 获得一个连接的socket描述符，处理相应的服务
    if len(sys.argv) != 2:          # [0]为.py文件名，[1]为socket描述符
        print RuntimeError("socket is not set correctly!")
        exit(1)
    else:
        conn = sys.argv[1]
        s = Service(conn)
        s.welcome_program()
