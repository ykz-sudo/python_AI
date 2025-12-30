# 作者: 王道 龙哥
# 2025年12月27日09时31分02秒
# xxx@qq.com
class HouseItem:
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return f'家具:{self.name} 占地面积{self.area}'


class House:
    def __init__(self, house_type, area):
        """
        房子的初始化方法
        :param house_type: 房子类型
        :param area: 房子面积
        """
        self.house_type = house_type
        self.area = area
        self.free_area = area  # 初始剩余面积和面积一致
        self.item_list = []

    def __str__(self):
        # return ("户型：%s\n总面积：%.2f[剩余：%.2f]\n家具：%s"
        #         % (self.house_type, self.area,
        #            self.free_area, self.item_list))
        return "户型：{}\n总面积：{}[剩余：{}]\n家具：{}".format(self.house_type, self.area,
                                                             self.free_area, self.item_list)

    def add_item(self, item:HouseItem) -> None:
        """
        加注解的目的是为了提高编写代码效率
        :param item:
        :return:
        """
        # 判断剩余面积是否还可以放家具
        if self.free_area > item.area:
            self.item_list.append(item.name)
            self.free_area -= item.area  # 减去家具面积
        else:
            print('没地方放家具了')


if __name__ == '__main__':
    bed = HouseItem('席梦思', 4)
    chest = HouseItem('衣柜', 2)
    table = HouseItem('餐桌', 1.5)

    print(bed)
    print(chest)
    print('-' * 50)
    house = House('三室一厅', 80.0)
    print(house)
    house.add_item(bed)
    house.add_item(chest)
    print(house)
