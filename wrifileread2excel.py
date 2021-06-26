import sys
import xlwt
import xlrd
import re
import os
import difflib
import time
import sys
import glob
import xlsxwriter
import itertools

#remove beginning and end commas
def writetofile(fd,str):
    fd.write(str)

def writetostring(chassis, ip, blade, pname, sno, sname, ipaddr):
    #filename = "C:\\t-mobile\\csv-files\\" + str(ip) + ".csv"
    file1 = "C:\\t-mobile\\csv-files\\output-" + str(ip) + ".csv"
    #print(sname)
    #print(ipaddr)
    with open(file1, "a+") as fout:
        str1 = str(chassis) + "," + str(ip) + "," + str(blade) + "," + str(pname) + "," + str(sno) + "," + str(sname) + "," + str(ipaddr)+"\n"
        fout.write(str1)
        fout.close()

def getBladeNum(line):
    string = re.findall(r'Server Blade #', line)
    if string:
        blade = int(line[len("Server Blade #")]+line[len("Server Blade #")+1])
        return blade

def getstrlen(string):
    counter=0
    for i in string:
        counter += 1
    return counter

def comparestrings(str1,str2):
    if str2 in str1:
        return 1

#check for server blade and subsequent lines
def checkServerBlade(line):
    if "Server Blade #" in line:
        blade = line.split(" ")[2].split("#")[1]
        return blade.strip()

def getChassisinfo(line):
    if "-adm-ilo [SCRIPT MODE]> show server info all" in line:
        chassis = line.split(" ")[0].split("-")[0]
        if chassis is not None:
            return chassis
    else:
        if "[SCRIPT MODE]> show server info all" in line:
            chassis = line.split(" ")[0]
            if chassis is not None:
                return chassis

def getProductName(line):
    if "Product Name:" in line:
        pname = line.strip().split(":")[1]
        return pname.strip()

def getSerialNumber(line):
    if "Serial Number:" in line:
       sno = line.strip().split(":")[1]
       if bool(sno):
          return sno.strip()
       else:
           sno = "None"
           return sno

def getServerName(line):
    if "Server Name:" in line:
       servername = line.strip().split(":")[1]
       if bool(servername):
           return servername.strip()
       else:
          servername = "None"
          return servername

def getIPAddress(fd):
    fname = os.path.basename(fd.name)
    ipaddress = fname.split(".")[0]+"."+fname.split(".")[1]+"."+fname.split(".")[2]+"."+fname.split(".")[3]
    return ipaddress.strip()

def getServerBladeType(line):
    if "Type:" in line:
        if "Server Blade Type:" not in line:
            servertype = line.strip().split(":")[1]
            ret = comparestrings(servertype, "Server Blade")
            if ret is not None:
                if servertype is not None:
                    return servertype

def checkServerType(str):
    if "Server Blade" in str:
        return 1

def getmgmtipaddress(line):
    ipaddress = line.strip().split(":")[1]
    if ipaddress is not None:
        return ipaddress.strip()
    else:
        ipaddress = "None"
        return ipaddress

def getotherinfo(chassis,ip,blade,line,fd):
    line = fd.readline()
    line = fd.readline()
    pname = getProductName(line)
    line = fd.readline()
    line = fd.readline()
    line = fd.readline()
    sno = getSerialNumber(line)
    #print(sno)
    line = fd.readline()
    line = fd.readline()
    sname = getServerName(line)
    for i in range(25):
        line = next(fd).strip()
        if "IP Address: " in line:
            ipaddr = getmgmtipaddress(line)
    writetostring(chassis, ip, blade, pname, sno, sname, ipaddr)

def readinputfile(file):
    with open(file, "r", encoding="Latin-1") as fd:
       ipaddress = getIPAddress(fd)
       line = fd.readline()
       chassis=0
       while line:
          if (chassis==0):
             chassisinfo = getChassisinfo(line)
             if chassisinfo is not None:
                 chassis=1
          blade = checkServerBlade(line)
          if blade is not None:
                line = fd.readline()
          servertype = getServerBladeType(line)
          if servertype is not None:
               ret = checkServerType(servertype)
               if ret == 1:
                  getotherinfo(chassisinfo, ipaddress, blade, line,fd)
          line = fd.readline()
    fd.close()

def singlefileread():
    file="C:\\t-mobile\BIC_jay\COMMAND\LOG\OA_show server info all\\20210204_921\\5.232.106.8.wri"
    readinputfile(file)

def multiplefileread():
    path="C:\\t-mobile\BIC_jay\COMMAND\LOG\OA_show server info all\\20210204_921\\*.wri"
    print(path)
    files = glob.glob(path)
    for file in files:
       readinputfile(file)

if __name__ == "__main__":
    #singlefileread()
    multiplefileread()