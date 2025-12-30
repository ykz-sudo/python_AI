# 作者: 王道 龙哥
# 2025年12月30日10时33分09秒
# xxx@qq.com

def while_read():
    file = open('file.txt', 'r', encoding='utf8')
    while True:
        txt = file.read(5)  # 光标在文件末尾时，读取就会得到空字符串
        if not txt:  # 空字符串是假
            break
        print(txt, end='')
    file.close()


def while_readline():
    file = open('file.txt', 'r', encoding='utf8')
    while True:
        txt = file.readline()  # 光标在文件末尾时，读取就会得到空字符串
        if not txt:  # 空字符串是假
            break
        print(txt, end='')
    file.close()


def use_readlines():
    file = open('file.txt', 'r', encoding='utf8')
    list_txt = file.readlines()  # 光标在文件末尾时，读取就会得到空字符串
    print(list_txt)
    file.close()


def use_writelines():
    lines = ["张三,20\n", "李四,19\n", "王五,21\n"]  # 列表元素带换行符
    f = open("student.txt", "w", encoding="utf-8")
    f.writelines(lines)  # 一次性写入列表
    f.close()


if __name__ == '__main__':
    # while_read()
    # while_readline()
    # use_readlines()
    use_writelines()