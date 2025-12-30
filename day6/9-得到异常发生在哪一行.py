# 作者: 王道 龙哥
# 2025年12月29日11时06分53秒
# xxx@qq.com
# 作者: 王道 龙哥
# 2025年12月29日10时51分18秒
# xxx@qq.com
import my_module
def divide(a):
    try:
        result=my_module.func1(a)
    except ZeroDivisionError:
        print('发生除0异常')
    except Exception as e:
        print(e)  # 不知道什么类型异常，打印异常（记日志）
        print(e.__traceback__.tb_lineno)  # 获取异常发生的行数
        print(e.__traceback__.tb_frame.f_globals['__file__'])  # 获取异常发生的文件名
    else:
        print('没有发生异常')
        return result
    finally:
        print('是否有异常代码都会走下来,有return我还是会执行')


ret = divide(3)
print(ret)
