import timeit

# 1. 基础语法对比
name = "Alice"
age = 30

# format 方法
str_format = "My name is {} and I am {} years old.".format(name, age)
# format 位置参数
str_format_pos = "My name is {0} and I am {1} years old. {0} likes Python.".format(name, age)
# format 关键字参数
str_format_key = "My name is {n} and I am {a} years old.".format(n=name, a=age)

# f-string
str_fstring = f"My name is {name} and I am {age} years old."

print("--- 基础语法 ---")
print(f"format: {str_format}")
print(f"f-string: {str_fstring}")

# 2. 表达式求值
print("\n--- 表达式求值 ---")
# format 需要在外部计算
width = 5
height = 10
print("Area (format): {}".format(width * height))

# f-string 可以直接在占位符中计算
print(f"Area (f-string): {width * height}")
print(f"Is age > 18? {age > 18}")

# 3. 格式化控制 (数字精度、填充对齐)
pi = 3.1415926535
print("\n--- 格式化控制 ---")
# format
print("PI (format): {:.2f}".format(pi))
print("Padding (format): {:>10}".format("test"))

# f-string
print(f"PI (f-string): {pi:.2f}")
print(f"Padding (f-string): {'test':>10}")

# 4. 字典访问
person = {'name': 'Bob', 'age': 25}
print("\n--- 字典访问 ---")
# format
print("Person (format): {p[name]} is {p[age]}".format(p=person))
# f-string (注意引号嵌套)
print(f"Person (f-string): {person['name']} is {person['age']}")

# 5. 性能对比
print("\n--- 性能对比 (执行 1,000,000 次) ---")
setup = 'name = "Alice"; age = 30'
stmt_format = '"My name is {} and I am {} years old.".format(name, age)'
stmt_fstring = 'f"My name is {name} and I am {age} years old."'

time_format = timeit.timeit(stmt_format, setup=setup, number=1000000)
time_fstring = timeit.timeit(stmt_fstring, setup=setup, number=1000000)

print(f"format() time: {time_format:.4f} seconds")
print(f"f-string time: {time_fstring:.4f} seconds")
print(f"f-string is {time_format / time_fstring:.2f}x faster")
