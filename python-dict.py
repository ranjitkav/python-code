#!/usr/bin/python3

mydict = {
    "brand": "Honda",
    "model": "CRV",
    "year": 2015
}

print (mydict)
print ("Model is:", mydict["model"])
print ("Value if model key is:", mydict.get("model"))
mydict["year"] = 2014
print("Updated dictionary is:", mydict)

# loop though dictionary
print("Looping through dictionary")
for i in mydict:
    print(i)

# print all values in the dictionary
print("Printing all values in the dictionary")
for i in mydict:
    print(mydict[i])

# print all values using .values
print("Printing all values using .values")
for i in mydict.values():
    print(i)

# Loop through both keys and values using items method
print("Loop through keys and values using items")
for i, j in mydict.items():
    print(i,j)

# check if key exists
print("Check if key exists")
if "condition" in mydict:
    print("Yes, 'condition' is one of the keys in mydict")
    print("removing condition key using pop")
    mydict.pop("condition")
    print ("Updated dictionary is: ", mydict)
else:
    print("No, 'condition' is not one of the keys in mydict")
    print("Adding condition key")
    mydict["condition"] = "Good"
    print ("Updated dictionary is: ", mydict)

# remove last inserted using popitem
print("Removing last inserted item with popitem")
mydict.popitem()
print ("Updated dictionary is: ", mydict)
