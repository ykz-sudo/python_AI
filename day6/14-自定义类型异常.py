# 作者: 王道 龙哥
# 2025年12月29日14时33分03秒
# xxx@qq.com
class UsernameError(Exception):
    def __init__(self):
        pass  # 空实现，使用默认的异常行为


class PasswordError(Exception):
    def __init__(self, length, min_len=8, max_len=10):
        self.length = length  # 保存错误的值
        self.min_len = min_len
        self.max_len = max_len

        # 调用父类的__init__，设置异常描述信息（通过super()传递）
        super().__init__(f'密码长度不合法,长度必须在{min_len} ~ {max_len} 之间，你的长度是{self.length}')


def login():
    username = input("请输入用户名:")
    password = input("请输入密码:")

    # 长度必须在 3-8位之间
    if len(username) < 3 or len(username) > 8:
        raise UsernameError()

    if len(password) < 8 or len(password) > 10:
        raise PasswordError(len(password))


if __name__ == '__main__':
    try:
        login()
    except UsernameError:
        print("用户名不合法")
    except PasswordError as e:
        print(e)
    # 兜底
    except Exception as e:
        print(e)
    else:
        print("用户名和密码都合法，校验通过...")
