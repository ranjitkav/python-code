#!/usr/bin/python3

class myClass:
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def myfunc(abc):
     print("Name is: ", abc.name)

obj = myClass("Ranjit", 44)

print("Name is:", obj.name)
print("Age is:",  obj.age)
print("obj is:", obj.myfunc())

#modify object
obj.age = 45
print("Age is:",  obj.age)

#delete property
del obj.age
del obj





