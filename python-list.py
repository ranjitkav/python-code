#!/usr/bin/python3

fruitslist = ["apple", "banana", "mango", "guava", "orange", "apple"]
fruits = {"apple", "banana", "mango", "guava", "orange", "apple"}
print ("Fruits list is:",fruitslist)
print ("first item is:",fruitslist[0])
# to print last item
print ("last item is:",fruitslist[-1])
print ("2nd last item is:",fruitslist[-2])
print ("Range from 2 to 5", fruitslist[2:5])

fruitlist = list(fruitslist)
fruitlist[1] = "kiwi"
flist = tuple(fruitlist)

print ("list is:", fruitlist)
print ("tuple is:", flist)
print ("Length of list is:", len(fruitlist))
print ("Length of tuple is:", len(flist))

#sets
fruits.add("grapes")
print ("new fruitslist is:", fruits)
fruits.remove("apple")
print ("new fruitslist after removing is:", fruits)

# print list using for loop
print ("Printing fruitslist using for loop")
for i in fruitslist:
   print(i)
j = 0
# print using while loop
print ("Printing fruitslist using while loop")
while j < 6:
  print (fruitslist[j])
  if j == 6:
      break
  j +=1

