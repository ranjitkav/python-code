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

chassisinfo = ""

#remove beginning and end commas
def writetofile(fd,str):
    fd.write(str)

def writetostring(chassis, ip, blade, pname, sno, sname, ipaddr):
    #filename = "C:\\t-mobile\\csv-files\\" + str(ip) + ".csv"
    file1 = "C:\\t-mobile\\csv-files\\output-" + str(ip) + ".csv"
    #print(sname)
    #print(ipaddr)
    with open(file1, "a+") as fout:
        if ipaddr != None:
           str1 = str(chassis) + "," + str(ip) + "," + str(blade) + "," + str(pname) + "," + str(sno) + "," + str(sname) + ","+ str(ipaddr)
        else:
           str1 = str(chassis) + "," + str(ip) + "," + str(blade) + "," + str(pname) + "," + str(sno) + "," + str(sname) + "," + str(ipaddr)+"\n"
        print(str1)
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
        b1 = line[getstrlen("Server Blade #")]
        b2 = line[getstrlen("Server Blade #") + 1]
        blade = b1 + b2
        return blade

def getChassisinfo(line):
    if "-adm-ilo [SCRIPT MODE]> show server info all" in line:
         chassis = line[0:(getstrlen(line) - getstrlen("-adm-ilo [SCRIPT MODE]> show server info all"))]
         if chassis is not None:
            return chassis
    else:
        if "[SCRIPT MODE]> show server info all" in line:
            chassis = line[0:(getstrlen(line) - getstrlen("   [SCRIPT MODE]> show server info all"))]
            if chassis is not None:
                return chassis

def getProductName(line):
    if "Product Name:" in line:
         pname = line[getstrlen("Product Name: "):getstrlen(line)-1]
         if pname is not None:
             pname = pname[1:]
             return pname

def getSerialNumber(line):
    if "Serial Number:" in line:
       sno = line[getstrlen("Serial Number: "):getstrlen(line)]
       if sno is not None:
           sno = sno[1:]
       if "[" in sno:
           sno = sno[1:]
       if "]" in sno:
           sno = sno[:-1]
       if "Unknown" in sno:
           sno = sno[:-7]
       sno = sno[:-1]
       return sno

def getServerName(line):
    if "Server Name:" in line:
       servername = line[getstrlen("Server Name: "):getstrlen(line)-1]
       if servername == ' ':
           servername = None
           return servername
       servername = servername[1:]
       if "[" in servername:
           servername = servername[1:]
       if "]" in servername:
           servername = servername[:-1]
       return servername

def getIPAddress(fd):
    fname = os.path.basename(fd.name)
    ipaddress = fname[0:(len(fname) - len(".wrt"))]
    return ipaddress

def getServerBladeType(line):
    if "Type:" in line:
        if "Server Blade Type:" not in line:
            servertype = line[getstrlen("Type: "):getstrlen(line)]
            ret = comparestrings(servertype, "Server Blade")
            if ret is not None:
                if servertype is not None:
                    return servertype

def checkServerType(str):
    if "Server Blade" in str:
        return 1

def getmgmtipaddress(line):
    if "IP Address:" in line:
        ipaddress = line[getstrlen("IP Address:  "):getstrlen(line)]
        if ipaddress is not None:
           return ipaddress
        else:
            ipaddress = None
            return ipaddress
    else:
        ipaddress = None
        return ipaddress

def getotherinfo(chassis,ip,blade,line,fd):
    line = fd.readline()
    line = fd.readline()
    pname = getProductName(line)
    #print(pname)
    #print("Length of pname is:"+ getstrlen(pname))
    line = fd.readline()
    line = fd.readline()
    line = fd.readline()
    sno = getSerialNumber(line)
    #print(sno)
    line = fd.readline()
    line = fd.readline()
    sname = getServerName(line)
    #print(sname)
    for i in range(25):
       line = fd.readline()
       if "IP Address: " in line:
           break
       i += 1
    ipaddr = getmgmtipaddress(line)
    writetostring(chassis, ip, blade, pname, sno, sname, ipaddr)
    #writetostring(chassis,ip,blade,pname,sno,sname,"\n")

# main code
# read lines from input file
def readinputfile(file):
    with open(file, "r") as fd:
       ipaddress = getIPAddress(fd)
       line = fd.readline()
       chassis=0
       while line:
          if (chassis==0):
             chassisinfo = getChassisinfo(line)
             if chassisinfo is not None:
                 #print(chassisinfo)
                chassis=1
          blade = checkServerBlade(line)
          if blade is not None:
                #print(blade)
                #check for further lines after blade
                line = fd.readline()
          servertype = getServerBladeType(line)
          if servertype is not None:
               ret = checkServerType(servertype)
               if ret == 1:
                  getotherinfo(chassisinfo,ipaddress, blade, line,fd)
                  #buf = writetostring(chassisinfo, ipaddress, blade,sno, sname )
          line = fd.readline()
    fd.close()

# combine csv files
def combinecsvfiles():
    import pandas as pd
    path = "C:\\t-mobile\\csv-files\\"
    print(path)
    all_files = glob.glob(os.path.join(path, "*.csv"))
    writer = pd.ExcelWriter('C:\\t-mobile\\combinedcsv.xlsx', engine='xlsxwriter')
    for file in all_files:
        #print(file)
        df = pd.read_csv(file)
        df.to_excel(writer, index=False, sheet_name=os.path.basename(file))
    writer.save()

# main code
# read lines from input file
path = "C:\\t-mobile\\BIC_jay 2\\BIC_jay\\COMMAND\\LOG\\OA_show server info all\\20210118_1655\\*.wri"
#print(path)
files = glob.glob(path)
for file in files:
  # print(file)
#file = "C:\\t-mobile\\BIC_jay 2\\BIC_jay\\COMMAND\\LOG\\OA_show server info all\\20210118_1349\\5.209.37.93.wri"
  readinputfile(file)
  #print(file)
#combinecsvfiles()

