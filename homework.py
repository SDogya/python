def prime_test(l): # тест простоты
    for i in range(3, int(l ** .5) + 1, 2):
        if l % i == 0:
            return False
    return True


def euclidus(a: int, b: int):  # евклид
    while b:
        a, b = b, a % b
    return abs(a)


def extended_euclidus(a: int, b: int): # расширенный евклид
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, a, b = b // a, b % a, a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0, y0


class Quaternion: # кватернионы
    def __init__(self, args: list):
        if len(args) < 5:
            self.x = list(args)

        else:
            raise TypeError("fuck")

        while len(self.x) < 4:
            self.x.append(0)

        self.el = ["", "i", "j", "k"]

    def __mul__(self, other):
        if type(other) == q:
            table = [
                [q([1]), q([0, 1]), q([0, 0, 1]), q([0, 0, 0, 1])],
                [q([0, 1]), q([-1]), q([0, 0, 0, 1]), q([0, 0, -1])],
                [q([0, 0, 1]), q([0, 0, 0, -1]), q([-1]), q([0, 1])],
                [q([0, 0, 0, 1]), q([0, 0, 1, 0]), q([0, -1, 0, 0]), q([-1])]
            ]
            x = q([])
            for i in range(4):
                for j in range(4):
                    x += self.x[i] * other.x[j] * table[i][j]
            return x


        elif type(other) in [int, float]:

            return q([self.x[0] * other, self.x[1] * other, self.x[2] * other, self.x[3] * other])

        else:
            raise TypeError("fuck your type, i need q type or number")

    def __rmul__(self, other):
        return q(self.x) * other

    def __str__(self):
        s = ""
        for i in range(4):
            if i == 0:
                s += str(self.x[i])
            else:
                if self.x[i] != 0:
                    s += " + " if self.x[i] > 0 else " - "
                    s += str(abs(self.x[i])) + self.el[i]
        return s

    def __abs__(self):
        s = 0
        for i in self.x:
            s += i ** 2
        return s ** 0.5

    def __add__(self, other):
        if type(other) == q:
            for i in range(4):
                self.x[i] += other.x[i]
            return q(self.x)
        else:
            raise TypeError("fuck your type, i need q type")

    def __sub__(self, other):
        if type(other) == q:

            return q(self.x) + other * -1
        else:
            raise TypeError("fuck your type, i need q type")

    def conjugate(self):

        x = q(self.x)*q([-1])
        x.x[0]*=-1
        return x

    def __list__(self):
        return self.x

   
