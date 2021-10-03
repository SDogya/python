import numpy

def fact(n):
    x = 1
    c = 1
    while x < n + 1:
        c *= x
        x += 1
    return c

def Binomial(k,n):
    if k>=n :
        return fact(k)/(fact(n)*(fact(k-n)))
    else:
        return 0

def ber_number(n):
    if n==0:
        return 1

    S=-1/(n+1)
    k=1
    s=0
    while k<= n:
          s+=Binomial(n+1,k+1)*ber_number(n-k)
          k+=1
    return S*s


def tan(x):
    """
    Вычисление тангенс при помощи частичного суммирования
    ряда Тейлора для окрестности 0
    """
    iter =11
    n=1
    s=0
    while n<=iter:
       s+=(ber_number(2*n)*((-4)**n) *(1-4**n)*(x**(2*n-1)))/(fact(2*n))
       n+=1
    return s

x = numpy.pi/3
print(tan(x))
print(numpy.tan(x))

