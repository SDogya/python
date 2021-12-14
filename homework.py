def prime_test(l):
    for i in range(3, int(l ** .5) + 1, 2):
        if l % i == 0:
            return False
    return True


def euclidus(a: int, b: int):
    while b:
        a, b = b, a % b
    return abs(a)


def extended_gcd(a: int, b: int):
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, a, b = b // a, b % a, a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0, y0


class quaternion:
    def __init__(self, args: list):
        if len(args) < 5:
            self.x = list(args)

        else:
            raise TypeError("fuck")

        while len(self.x) < 4:
            self.x.append(0)

        self.el = ["", "i", "j", "k"]

    def __mul__(self, other):
        if type(other) == quaternion:
            table = [
                [quaternion([1]), quaternion([0, 1]), quaternion([0, 0, 1]), quaternion([0, 0, 0, 1])],
                [quaternion([0, 1]), quaternion([-1]), quaternion([0, 0, 0, 1]), quaternion([0, 0, -1])],
                [quaternion([0, 0, 1]), quaternion([0, 0, 0, -1]), quaternion([-1]), quaternion([0, 1])],
                [quaternion([0, 0, 0, 1]), quaternion([0, 0, 1, 0]), quaternion([0, -1, 0, 0]), quaternion([-1])]
            ]
            x = quaternion([])
            for i in range(4):
                for j in range(4):
                    x += self.x[i] * other.x[j] * table[i][j]
            return x


        elif type(other) in [int, float]:

            return quaternion([self.x[0] * other, self.x[1] * other, self.x[2] * other, self.x[3] * other])

        else:
            raise TypeError("fuck your type, i need quaternion type or number")

    def __rmul__(self, other):
        return quaternion(self.x) * other

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
        if type(other) == quaternion:
            for i in range(4):
                self.x[i] += other.x[i]
            return quaternion(self.x)
        else:
            raise TypeError("fuck your type, i need quaternion type")

    def __sub__(self, other):
        if type(other) == quaternion:

            return quaternion(self.x) + other * -1
        else:
            raise TypeError("fuck your type, i need quaternion type")

    def conjugate(self):

        x = quaternion(self.x) * quaternion([-1])
        x.x[0]*=-1
        return x

    def __list__(self):
        return self.x



x = quaternion([1, 1, 1, 1])
y = quaternion([1, 1, 1, 1])
print( x+y*x)
print(euclidus(83,7))
print(extended_gcd(83,7))
print(prime_test(5489251893))
