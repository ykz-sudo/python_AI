file = open('my_conf.txt', 'r', encoding='utf8')
txt = file.read()
file.close()
my_dict = eval(txt)  # 把配置文件中的字符串变为字典
print(type(my_dict))
print(my_dict)
