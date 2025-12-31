import types
import os
import sys
import re


# class MyClass:
#     def __new__(cls, *args, **kwargs):
#         # 虽然看起来有 cls 参数，但它被 Python 特殊处理
#         print(f"cls 参数类型: {type(cls)}")
#         return super().__new__(cls)
#
#     @staticmethod
#     def static_method():
#         # 这才是普通的静态方法
#         return "static method"
#
#
# # 检查方法类型
#
#
# print(f"__new__ 是静态方法: {isinstance(MyClass.__new__, types.FunctionType)}")
# print(f"static_method 是静态方法: {isinstance(MyClass.static_method, types.FunctionType)}")
#
# # 实际上，__new__ 是一个普通的函数
# # 直到被 Python 解释器特殊处理
# myclass = MyClass()
# print(type(MyClass))
# print(type(myclass))


def open_r():
    with open('file.txt', 'r', encoding='utf-8') as f:
        txt = f.read()
        print(txt)


def open_w():
    with open('file2.txt', 'w', encoding='utf8') as f:
        f.write('我能打上海major\n')
        f.write('文件自动关闭，稳稳的幸福')


def dir_op():
    for file in os.listdir('.'):
        print(file)
    os.chdir('dir1')
    print(os.getcwd())
    os.chdir('..')
    print(os.getcwd())


def use_seek():
    with open('file.txt', 'a+', encoding='utf-8') as f:
        f.write('我好帅')
        txt = f.read()
        print(txt)
        f.seek(3, os.SEEK_SET)
        txt = f.read()
        print(txt)


def use_re1():
    pattern = r"[a-zA-Z]\d\s\W"
    texts = ['12 1', 'a5 f1', 'abc))', 'a3 &&985']
    for text in texts:
        result = re.match(pattern, text)
        if result:
            print(f'{text} 匹配成功 {result.group()}')
        else:
            print(f'{text} 匹配失败')


def use_re2():
    pattern = r'\d+$'
    texts = ['1234', 'a666', '00a09', '114514']
    for text in texts:
        result = re.match(pattern, text)
        if result:
            print(f'{text} 匹配成功 {result.group()}')
        else:
            print(f'{text} 匹配失败')


def use_re3():
    original_data = 'ykongze@gmail.com'
    pattern = r'\d+$'
    texts = ['1234', 'a666', '00a09', '114514&985abc', 'abc123']
    for text in texts:
        result = re.search(pattern, text)
        if result:
            print(f'{text} 匹配成功 {result.group()}')
        else:
            print(f'{text} 匹配失败')


def use_re4():
    email = '我的谷歌邮箱是ykongze@gmail.com，QQ邮箱是507911754@qq.com'
    pattern = r'(\w+@\w+\.\w+)'
    result = re.findall(pattern, email, flags=re.ASCII)
    if result:
        print(f'{email} 匹配成功 {result}')
    else:
        print(f'{email} 匹配失败')


def dir_scan(path, left_width):
    """
    目录深度优先遍历
    :return:
    """

    all_files = os.listdir(path)
    os.chdir(path)
    for file in all_files:
        print(left_width * ' ', file)
        if os.path.isdir(file):
            dir_scan(file, left_width + 4)
    os.chdir('..')


if __name__ == '__main__':
    open_r()
    print('-' * 50)
    open_w()
    dir_op()
    print('-' * 50)
    print(sys.argv)
    print('-' * 50)
    use_re1()
    print('-' * 50)
    use_re2()
    print('-' * 50)
    use_re3()
    print('-' * 50)
    use_re4()
    print('-' * 50)
    use_seek()
    print('-' * 50)
    dir_scan('.', 0)
