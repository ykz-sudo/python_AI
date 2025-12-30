# 作者: 王道 龙哥
# 2025年12月29日10时51分18秒
# xxx@qq.com
def divide(a):
    try:
        b = int(input('请输入一个数'))
        result = a / b
        print(f'result={result}')
    except ZeroDivisionError:
        print('发生除0异常')
    except ValueError:
        print('请输入整数')
    else:
        print('没有发生异常')
        return result
    finally:
        print('是否有异常代码都会走下来,有return我还是会执行')


ret = divide(3)
print(ret)
