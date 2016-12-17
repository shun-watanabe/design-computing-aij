from rect import *  # rect.pyの内容をインポートする


class Square(Rectangle):

    def __init__(self, dx):
        self.dx = dx
        self.dy = self.dx  # 2辺の長さを等しくする

sq1 = Square(100)
print('Area of sq1: ', sq1.area())
