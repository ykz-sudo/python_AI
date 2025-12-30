# 作者: 王道 龙哥
# 2025年12月29日14时20分10秒
# xxx@qq.com

def get_password(a):
    password = input("请输入密码:")

    # 如果密码长度小于8，抛出异常
    if len(password) < 8:
        raise Exception('密码长度小于8位')
    return password


try:
    password2 = get_password()
    print(password2)
except Exception as e:
    print(e)
