# 作者: 王道 龙哥
# 2025年12月29日10时30分32秒
# xxx@qq.com
class MusicPlayer(object):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, name):
        self.music_name = name


music_player1 = MusicPlayer('双节棍')
music_player2 = MusicPlayer('孤勇者')
print(music_player1)
print(music_player2)
print(music_player2.music_name)
print(music_player1.music_name)

print(music_player1 is music_player2)

