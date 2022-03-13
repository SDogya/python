import time

from numba import jit, njit  # type: ignore

N = 10000032
I = 100000


@jit(nopython=True)
def fast_shit_func(n, i):
    s = 1
    for j in range(n):
        s += s ** i

        s =s**(1 / (i ))
    return s


@njit()
def fast_as_fuck_shit_func(n, i):
    s = 1
    for j in range(n):
        s += s ** i

        s =s**(1 / (i ))
    return s


@njit(fastmath=True)
def faster_then_fast_as_fuck_shit_func(n, i):
    s = 1
    for j in range(n):
        s += s ** i

        s = s ** (1 / (i))
    return s


def shit_func(n, i):
    s =1
    for j in range(n):
        s += s**i

        s = s ** (1 / (i))
    return s


t=time.time_ns()
print(shit_func(N,I))
print(-(t-time.time_ns()))
t = time.time_ns()
print(fast_shit_func(N, I))
print(-(t - time.time_ns()))

t = time.time_ns()
print(fast_as_fuck_shit_func(N, I))
print(-(t - time.time_ns()))

t = time.time_ns()
print(faster_then_fast_as_fuck_shit_func(N, I))
print(-(t - time.time_ns()))

