import os
import sys

def getstrlen(string):
    counter=0
    for i in string:
        counter += 1
    return counter

def getlistofemail(line,emaillist):
    if "email:" in line:
        emaillist.append(line[getstrlen("email: "):getstrlen(line)].strip('\n'))

def getlistofservers(line,serverlist):
    if "server:" in line:
        serverlist.append(line[getstrlen("server: "):getstrlen(line)].strip('\n'))

with open("config.txt", "r") as fd:
    serverlist = []
    emaillist = []
    line = fd.readline()
    while line:
        getlistofservers(line,serverlist)
        getlistofemail(line,emaillist)
        line = fd.readline()
    print(serverlist)
    print(emaillist)