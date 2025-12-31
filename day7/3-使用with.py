def use_with():
    with open('file.txt', 'r', encoding='utf8') as f:
        txt = f.read()
        print(txt)


if __name__ == '__main__':
    use_with()
