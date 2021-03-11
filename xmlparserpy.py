import xml.etree.ElementTree as ET
import glob
import os

class hostEntry:
    def __init__(self,inString):
       splitString = inString.split()
       self.site=splitString[1][3:5].lower()
       self.hostName=splitString[1].lower()
       self.hostIP=splitString[0]
       self.nodeType=splitString[1][0:3].lower()

class PMMOResultEntry:
    def __init__(self):
        self.DN = ""
        self.measurementType = ""
        self.counterList = []

class measCount:
    def __init__(self, inString):
        splitString = inString.split(',')
        self.nodeType = splitString[0].strip()
        self.nds9sp2adm = int(splitString[1].strip())
        self.nds9sp2netact = int(splitString[2].strip())
        self.nds16adm = int(splitString[3].strip())
        self.nds16netact = int(splitString[4].strip())
        self.nds17adm = int(splitString[5].strip())
        self.nds17netact = int(splitString[6].strip())

class attribute:
        counterName = ""
        counterValue = ""

# no need of getPmDatafromAdm as files are already fetched
class PMMOResultEntry:
    def __init__(self):
        self.DN = ""
        self.measurementType = ""
        self.counterList = []

def processPmDatabackup(nodeName):
    print("Processing pm data")
    tempPrintList = []
    filteredList = [x for x in pmmo if nodeName.lower() in x.DN]
    #for x in pmmo:
    #    if nodeName.lower() in x.DN:
    #        filteredList.append(x)
    for x in filteredList:
        tempPrintList.append(x.DN.ljust(65)+x.measurementType.ljust(20)+ str(len(x.counterList)).ljust(10))
    tempPrintList.sort()
    for x in tempPrintList: print(x)
    # get total count
    newlist = [x for x in pmmo if node.lower() in x.DN]
    totalcount=0

# process pm data
def processPmData(nodeName):
    print("Processing pm data")
    # get hosts info
    nodeinfo="C:\\scripts\\conf\\ndsNodes1.txt"
    hostlistall = [ hostEntry(line) for line in open(nodeinfo, "r") if (line != '\n') and (line.startswith("#") != 1)]
    if nodeName != "all":
       tempPrintList = []
       filteredList = [x for x in pmmo if nodeName.lower() in x.DN]
       for x in filteredList:
           tempPrintList.append(x.DN.ljust(65)+x.measurementType.ljust(20)+ str(len(x.counterList)).ljust(10))
       tempPrintList.sort()
       for x in tempPrintList: print(x)
    # get total count
    if nodeName == "all":
       hostlist = [x for x in hostlistall if x.hostName.lower().startswith(node)]
       hostlist.sort(key=lambda x:int(x.hostName[-3]))
       for item in hostlist:
           filteredList = [x for x in pmmo if item.hostName in x.DN]
           count=0
           for i in filteredList:
               count += i.counterList
           print(count)


def parseXMLfile():
    path = "C:\\scripts\\conf\\*.xml"
    # path = "PM-files/PM.5.232.106.109.20210304.142600.9.xml"
    files = glob.glob(path)
    # create empty list for new items
    global pmmo
    pmmo = []
    for file in files:
      # create element tree object
      print("Processing file:", file)
      tree = ET.parse(file)
      # get root element
      root = tree.getroot()
      # iterate new items
      for item in root:
          for pmmoResult in item.findall('PMMOResult'):
             tmpObject=PMMOResultEntry()
             tmpObject.counterList=[]
             for entry in pmmoResult:
                 if entry.tag=="MO":
                     for entry1 in entry:
                         tmpObject.DN = entry1.text.lower()
                 if entry.tag == "PMTarget":
                     tmpObject.measurementType = entry.attrib['measurementType']
                     for entry1 in entry:
                         tmpPair = attribute()
                         tmpPair.counterName = entry1.tag.strip()
                         tmpPair.counterValue = entry1.text.strip()
                         tmpObject.counterList.append(tmpPair)
             pmmo.append(tmpObject)
   #print("Number of entries in PMMO list is: ", str(len(pmmo)))

if __name__ == "__main__":
    #file = "C:\\scripts\\PM.10.169.78.40.20210304.140300.10.xml"
    #print(file)
    # Parse the XML file
    parseXMLfile()
    node="CBEDA004"
    processPmData(node)