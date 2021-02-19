import os
import sys

list1 = ['banana', 'apple', 'mango']
list2 = ["orange", "papaya", "grapes"]

list1.sort() # sort in ascending
list2.sort() # sort in ascending

list3 = list1+list2  #merge lists
list3.sort()  # default in ascending order

print(list1) # sorted list
print(list2) # sorted
print(list3) # merged

list1.sort(reverse=True)  # to sort in descending order
print(list1) # reversed


