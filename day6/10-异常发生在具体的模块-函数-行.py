# 作者: 王道 龙哥
# 2025年12月29日11时15分39秒
# xxx@qq.com
import my_module
def divide(a):
    try:
        result=my_module.func1(a)
    except ZeroDivisionError:
        print('发生除0异常')
    except Exception as e:
        tb = e.__traceback__ #调用函数栈

        # 一路走到 traceback 链的最后
        while tb.tb_next:
            tb = tb.tb_next

        filename = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno
        funcname = tb.tb_frame.f_code.co_name

        print(f"异常发生位置：{filename}:{lineno}，函数：{funcname}")
    else:
        print('没有发生异常')
        return result
    finally:
        print('是否有异常代码都会走下来,有return我还是会执行')


ret = divide(3)
print(ret)