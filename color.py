from PIL import Image

width = 400
height = 300



class Color:
    def __init__(self, r, g, b, a):
        self.pr = self.to_percentage(r)
        self.pg = self.to_percentage(g)
        self.pb = self.to_percentage(b)
        self.pa = self.to_percentage(a)

    def __str__(self):
        return f'({self.to_base(self.pr)}, {self.to_base(self.pg)}, {self.to_base(self.pb)}, {self.to_base(self.pa)})'

    def __add__(self, other):
        nc = Color(0, 0, 0, 0)
        nc.pa = 1 - (1 - self.pa) * (1 - other.pa)
        print(self.pa)
        nc.pr = self.pr * self.pa / nc.pa + other.pr * other.pa * (1 - self.pa) / nc.pa
        nc.pg = self.pg * self.pa / nc.pa + other.pg * other.pa * (1 - self.pa) / nc.pa
        nc.pb = self.pb * self.pa / nc.pa + other.pb * other.pa * (1 - self.pa) / nc.pa

        return nc

    @staticmethod
    def to_percentage(bn):
        return (bn / 255)

    @staticmethod
    def to_base(pn):
        return round(pn * 255)

    def get_rgba(self):
        return self.to_base(self.pr), self.to_base(self.pg), self.to_base(self.pb), self.to_base(self.pa)


# fg = Color(255, 30, 10, 100)
# bg = Color(0, 90, 225, 125)
# x = fg + bg
#
# print(f'{fg} and {bg} makes {fg + bg}')
#
#
# img1 = Image.new(mode="RGBA", size=(width, height), color=(fg.get_rgba()))
# img2 = Image.new(mode="RGBA", size=(width, height), color=(bg.get_rgba()))
# img3 = Image.new(mode="RGBA", size=(width, height), color=(x.get_rgba()))
#
# img1.show()
# img2.show()
# img3.show()
