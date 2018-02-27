# -*- coding:utf-8 -*-
import socket


def myRecv(conn):
    # 从一个连接读入数据
    try:
        length = int(conn.recv(10))       # 每个数据流前10位记录该段报文长度
        data = ""
        while length > 1024:
            data += conn.recv(1024)         # 取出下1024个字符
            length -= 1024
        data += conn.recv(length)           # 一定有length>0
        return data
    except ValueError:
        raise


if __name__ == "__main__":
    string = "abc1"
    d = raw_input()
    print d