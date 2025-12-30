import types


class MyClass:
    def __new__(cls, *args, **kwargs):
        # 虽然看起来有 cls 参数，但它被 Python 特殊处理
        print(f"cls 参数类型: {type(cls)}")
        return super().__new__(cls)

    @staticmethod
    def static_method():
        # 这才是普通的静态方法
        return "static method"


# 检查方法类型


print(f"__new__ 是静态方法: {isinstance(MyClass.__new__, types.FunctionType)}")
print(f"static_method 是静态方法: {isinstance(MyClass.static_method, types.FunctionType)}")

# 实际上，__new__ 是一个普通的函数
# 直到被 Python 解释器特殊处理
myclass = MyClass()
print(type(MyClass))
print(type(myclass))
