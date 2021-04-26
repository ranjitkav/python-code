def findoccurances(list):
    oddoccur = []
    evenoccur = []
    count = 1
    item = 0
    for item in range(len(list)-1):
        if item+1 == len(list)-1:
            # Handle last item
            if list[item+1] == list[item-1]:
                count += 1
                if count % 2 != 0:
                    oddoccur.append(list[item])
                else:
                    evenoccur.append(list[item])
        if list[item] == list[item+1]:
            count += 1
        else:
            if (count % 2) != 0:
               oddoccur.append(list[item])
            else:
               evenoccur.append(list[item])
              # reset count to 1
            count = 1
    print("Num which have odd occurances: ", oddoccur)
    print("Num which have even occurances: ", evenoccur)

# Driver program to test the above function
if __name__ == "__main__":
   list = [2,2,2,3,3,4,4,5,5,5,7,7,7,7,7]
   findoccurances(list)

