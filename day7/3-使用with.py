# 作者: 王道 龙哥
# 2025年12月30日10时46分11秒
# xxx@qq.com
def use_with():
    with open('file.txt', 'r', encoding='utf8') as f:
        txt = f.read()
        print(txt)


if __name__ == '__main__':
    use_with()
