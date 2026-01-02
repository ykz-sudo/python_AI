# 作者: 王道 龙哥
# 2026年01月02日09时30分58秒
# xxx@qq.com
import re


def use_next():
    """
    列表是可迭代对象，当我们对可迭代对象使用 iter(可迭代对象）就会得到一个迭代器
    迭代器next到最后以后，是不会移动到前面的
    :return:
    """
    my_list = [1, 2, 3, 4, 5]
    Iterator_obj1 = iter(my_list)
    Iterator_obj2 = iter(my_list)
    Iterator_obj3 = iter(Iterator_obj2)  # 迭代器执行iter返回的是自身
    # i = next(Iterator_obj)  # 返回当前指向的结果，并移动到下一个
    # print(i)
    # i = next(Iterator_obj)
    # print(i)
    for i in Iterator_obj1:
        print(i, end=' ')
    print()
    for i in Iterator_obj3:
        print(i, end=' ')
    print()


def find_second_match(pattern, text):
    matches = re.finditer(pattern, text)
    try:
        next(matches)
        second_match = next(matches)
        return second_match.group()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    use_next()
    text = "abc123def456ghi789"
    pattern = r"\d+"
    second_match = find_second_match(pattern, text)
    print(second_match)
