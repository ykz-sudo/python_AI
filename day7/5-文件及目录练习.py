# 作者: 王道 龙哥
# 2025年12月30日11时10分21秒
# xxx@qq.com
import os, sys
import time


def use_rename():
    os.rename('2.png', '3.png')


def use_remove():
    os.remove('2.png')


def use_dir():
    # os.rmdir('dir2')
    list_name = os.listdir('.')
    print(list_name)
    print(os.getcwd())
    os.chdir('dir1')
    f = open('image1.png', 'wb')
    f.close()
    os.chdir('../')
    print(os.getcwd())


def dir_scan(path, left_width):
    """
    目录深度优先遍历
    :param path:
    :return:
    """
    all_files = os.listdir(path)  # 得到path路径下的所有文件
    for file in all_files:
        print(left_width * ' ', file)  # 打印文件名,离左边有left_width个空格
        new_path = path + '/' + file  # 拼接一个正确的路径
        if os.path.isdir(new_path):  # 判断一个文件是否是文件夹
            dir_scan(new_path, left_width + 4)


def dir_scan1(path, left_width):
    """
    目录深度优先遍历
    :param path:
    :return:
    """
    all_files = os.listdir(path)  # 得到path路径下的所有文件
    os.chdir(path)
    for file in all_files:
        print(left_width * ' ', file)  # 打印文件名,离左边有left_width个空格
        if os.path.isdir(file):  # 判断一个文件是否是文件夹
            dir_scan1(file, left_width + 4)
    os.chdir('..')  # 回到父级目录


def use_stat():
    print(time.time())  # 距离1970年1月1号的秒数
    if len(sys.argv) > 1:
        file_stat = os.stat(sys.argv[1])
        print('size大小 {},uid拥有者 {},mtime最后修改时间 {}'.format(file_stat.st_size, file_stat.st_uid,
                                                                     file_stat.st_mtime))
        from time import strftime
        from time import gmtime
        gm_time = gmtime(file_stat.st_mtime)
        # 把秒数转为字符串时间
        print(strftime("%Y-%m-%d %H:%M:%S", gm_time))


def use_argv():
    print(sys.argv)


if __name__ == '__main__':
    # use_rename()
    # use_remove()
    # use_dir()
    # dir_scan1('.', 0)
    use_stat()
    # use_argv()
