# 作者: 王道 龙哥
# 2025年12月30日10时50分25秒
# xxx@qq.com
import os


def use_seek():
    """
    使用a+
    :return:
    """
    file = open('file.txt', 'a+', encoding='utf8')
    file.write('今天天气不错')
    # 进行偏移,offset偏移量，whence相对位置
    file.seek(3, os.SEEK_SET)  # 回到文件开头，如果是汉字，要是3的倍数
    txt = file.read()
    print(f'读取的内容是:{txt}')
    file.close()


def use_code():
    with open("gbk_file.txt", "w", encoding="gbk") as f:
        f.write("这是GBK编码的文件")


def word_count():
    """
    统计文件中的单词数目
    :return:
    """
    count = 0
    with open('file1.txt', 'r', encoding='utf8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            count += len(line.split())
    print(count)


if __name__ == '__main__':
    # use_seek()
    # use_code()
    word_count()