from decimal import *
from sympy import *

def factor(n):
    with localcontext() as ctx:
        ctx.prec = 62
        r = int(Decimal(n).sqrt())

        pl = []
        for i in range (1, 1000):
            p = r - i
            if isprime(p):
                pl.append(p)

        ql = []
        for i in range (1, 1000):
            q = r + i
            if isprime(q):
                ql.append(q)
        
        for p in pl:
            for q in ql:
                if p * q == n:
                    print("Found factors p: {}, q: {}".format(p, q))
                    return

factor(1233626153975765256832069105719625449453005007655647000923233367120767290238588667397052161653352801437540471197470570083267)


"""     l = []
    for i in range (1, 1000):
        l.append(r - i)
        l.append(r + i)

    primesieve(l)

def primesieve(l):
    for i in range(2, Decimal(n).sqrt() + 1):
        for j in range(0, len(l)):
            if l[j] != 0 and l[j] % i == 0:
                l[j] = 0 """