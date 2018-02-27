# -*- coding:utf-8 -*-


def encode(data):
    # 为输入的data加上10个字符的数据报长度信息
    length = str(data.__len__()).zfill(10)
    return length+data


if __name__ == "__main__":
    data ="abc"
    print encode(data)

