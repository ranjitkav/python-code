########################################################################
# python code for printing
# cidr prefix, subnet mask, total IPs and usuable IPs
# prefixes 32 to 20 are currently supported
# TBD:  add more prefixes
#########################################################################
###  for Linux add #/usr/bin/python #######
###  uncomment below line when running this code in Linux
### #!/usr/bin/python
import os
import sys

mask=""

def getsubnetmaskforCIDR(cidr):
    if "32" in cidr:
        mask="255.255.255.255"
    if "31" in cidr:
        mask="255.255.255.254"
    if "30" in cidr:
        mask="255.255.255.252"
    if "29" in cidr:
        mask="255.255.255.248"
    if "28" in cidr:
        mask="255.255.255.240"
    if "27" in cidr:
        mask="255.255.255.224"
    if "26" in cidr:
        mask="255.255.255.192"
    if "25" in cidr:
        mask="255.255.255.128"
    if "24" in cidr:
        mask="255.255.255.0"
    if "23" in cidr:
        mask="255.255.254.0"
    if "22" in cidr:
        mask="255.255.252.0"
    if "21" in cidr:
        mask="255.255.248.0"
    if "20" in cidr:
        mask="255.255.240.0"
    return mask

def getmul(cidr):
    if "32" or "31" or "30" or "29" or "28" or "27" or "26" or "25" or "24" in cidr:
        mul=1
    if "23" in cidr:
        mul=2
    if "22" in cidr:
        mul=4
    if "21" in cidr:
        mul=8
    if "20" in cidr:
        mul=16
    return mul

def computeTotalIPadd(num,mul):
    totalip=(256*mul)-int(num)
    return totalip

def computeusableIPadd(num,mul):
    totalip=(256*mul)-int(num)
    if totalip == 1 or totalip == 2:
       usableIP=totalip
    else:
       usableIP=totalip-2
    return usableIP

def getlastnoinsubnetmask(cidrprefix):
   mask=getsubnetmaskforCIDR(cidrprefix)
   num=mask.split(".",3)
   lastnum=num[3]
   mul=getmul(cidrprefix)
   print("CIDR prefix is: ", cidrprefix)
   print("Subnet mask is: ", mask)
   print("Total number of IPs: ", computeTotalIPadd(lastnum, mul))
   print("Total number of Usuable IPs: ", computeusableIPadd(lastnum,mul))
   print("\n")
   mask=""

def printall():
   list = [32,31,30,29,28,27,26,25,24,23,22,21,20]
   for i in list:
       getlastnoinsubnetmask(str(i))

def printforprefix():
    cidrprefix = input("Enter CIDR prefix as /prefix e.g. /32, /32, /28,..: ")
    if "/" not in cidrprefix:
        getlastnoinsubnetmask(cidrprefix)
    else:
        getlastnoinsubnetmask(cidrprefix[1:])

# use below code for a particular prefix
printforprefix()

# use below function to print all
#printall()





