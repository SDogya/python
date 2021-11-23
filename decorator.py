def repeat(n):
    def decor(func):
        def void(c):
            x = c
            for i in range(n):
                x = func(x)
            return x

        return void

    return decor


@repeat(8)
def plus_1(x):
    return x + 1


@repeat(8)
def mul_2(x):
    return x * 2


print(plus_1(3))  
print(mul_2(4))  
