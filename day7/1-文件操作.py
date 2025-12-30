# 作者: 王道 龙哥
# 2025年12月30日09时34分40秒
# xxx@qq.com

def open_r():
    file = open('file.txt', 'r', encoding='utf8')
    txt = file.read(4)  # 默认是全部读空
    print(txt)
    # file.write('心情非常好')
    file.close()


def open_w():
    """
    w会清空文件
    :return:
    """
    file = open('file.txt', 'w', encoding='utf8')
    file.write('紧跟直播坚持练习')
    file.close()


def open_a():
    """
    w会清空文件
    :return:
    """
    file = open('file.txt', 'a', encoding='utf8')
    file.write('按时午休，保持良好作息')
    file.close()


def open_r2():
    """
    使用r+
    :return:
    """
    file = open('file.txt', 'r+', encoding='utf8')
    file.write('你好')
    file.close()


def open_a2():
    """
    使用a+
    :return:
    """
    file = open('file.txt', 'a+', encoding='utf8')
    file.write('今天天气不错')
    txt = file.read()
    print(f'读取的内容是:{txt}')
    file.close()


def open_rb():
    """
    使用rb读取二进制文件
    :return:
    """
    file = open('1.png', 'rb')
    file_bytes = file.read()  # 默认是全部读空
    file1=open('2.png','wb')
    file1.write(file_bytes) #把字节流写入2.png
    file.close()
    file1.close()


if __name__ == '__main__':
    # open_r()
    # open_w()
    # open_a()
    # open_r2()
    # open_a2()
    open_rb()
