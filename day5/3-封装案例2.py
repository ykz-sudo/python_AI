# 作者: 王道 龙哥
# 2025年12月27日10时27分14秒
# xxx@qq.com
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance  # 私有属性（余额）,只可以在类内部访问

    # 提供公开接口查询余额
    def get_balance(self):
        return self.__balance

    def deposit(self, amount):
        """
        存钱
        :param amount:
        :return:
        """
        if amount > 0:
            self.__balance += amount
            print('存款成功')
        else:
            print('存款失败')

    def withdraw(self, amount):
        if 0 < amount < self.__balance:
            self.__balance -= amount
        print('取款成功')


if __name__ == '__main__':
    account = BankAccount(100)
    account.deposit(50)
    account.withdraw(30)
