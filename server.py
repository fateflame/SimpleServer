# -*- coding:utf-8 -*-
import socket
import sys
import subprocess
import multiprocessing
from myService import Service, fun


class User:
    def __init__(self, str):
        data = str.split()
        if data.__len__() != 3:
            raise IndexError('incompatible element numbers')
        self.account = data[0]
        self.password = data[1]
        self.time = data[2]


class MyServer:
    # 负责处理连接建立前的工作，每收到一个新的连接conn，启动一个新的线程并转交给Service模块处理
    def __init__(self, file_location="./database"):
        # 初始化本模块，并为Service类进行相应初始化
        self.__host = ''
        self.__port = 50018
        self.__backlog = 1  # maximum number of queued connections, usually [0,5]
        self.server_socket = None
        self.__service_list = {}  # 已建立的连接-对应子进程 列表
        Service._Service__data_location = file_location  # 用户相关数据的保存地址
        self.__read_data()
        self.__setup()

    @staticmethod
    def __read_data():
        try:
            f = open(Service._Service__data_location, 'r')
            user_data = f.readlines()
            # 将读入的每一行用户数据转换为dict的一条记录
            for user in user_data:
                try:
                    temp = User(user)
                    Service._Service__user_list[temp.account] = temp
                except IndexError:
                    print ("invalid user data")
            f.close()
        except IOError:
            print ("please check if the database location is correct!")
            exit(1)
        except ValueError:
            print ("cannot find the file, exit")
            exit(1)

    def __setup(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.__host, self.__port))
        self.server_socket.listen(self.__backlog)

        self.__listen()
        self.server_socket.close()

    def __listen(self):
        conn, addr = self.server_socket.accept()


    def __create_service(self, conn):
        p = multiprocessing.Process(target=fun, args=(conn,))
        return p
        # self.__service_list[conn] = subprocess.Popen('py', args='./myService')

if __name__ == "__main__":
    # print sys.argv
    if len(sys.argv) > 1:
        s = MyServer(sys.argv[1])
    else:
        s = MyServer()




