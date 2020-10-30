#!/usr/bin/python3

i = lambda a: a+10
print(i(5))

j = lambda a,b: a * b
print(j(5,6))

k = lambda a,b,c: a + b + c
print(k(1,2,3))

def myfunc(n):
    return lambda a: a * n

mydouble = myfunc(2)

print (mydouble(11))


