#!/ISS/nsncare/lang/python2.7.18/bin/python
##################################################################################################
#Program Name           : checkCountersinAdm.py
#Current version        : v1.0, Date: 05/28/2020
#Purpose                : To audit counters from ADM
#Code Written By        : Srinivasan Velayudham, srinivasan.velayudham@nokia.com, Nokia
#Usage                  : $ ./checkCountersinAdm.py
#Change History:        : v1.0 - Initial Version 
###################################################################################################
import os
import re
import sys
#import yaml
import json
import time
import gzip
import shutil
import random
import tarfile
import logging
import argparse
import commands
import socket
import traceback
import logging.config
import logging.handlers
import pexpect
import getpass
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.
    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.
    return file_paths  # Self-explanatory.

def cleanOldFiles(folderPath,noOfDays):
        appLog.info("Performing housekeeping. Deleting old files...")
	fileListResultsBackup = get_filepaths(folderPath)
	for fi1 in fileListResultsBackup:
                fileTime=datetime.fromtimestamp(os.path.getctime(fi1))
                currentTime=datetime.now()
                if fileTime < (currentTime-timedelta(days=int(noOfDays))):
                        appLog.info("Cleaning up the file, "+fi1 +". The file is older than "+ str(noOfDays)+ " days. This will be deleted")
                        os.remove(fi1)


def printReportHeaderXML():
	outFileXML.write("<!DOCTYPE html><html><head><style>table, th, td { border: 1px solid black;border-collapse: collapse;}th,td{padding: 5px;} th{ text-align: left;} table#t02 { background-color: #f1f1c1;}</style><title>One NDS - Trigger Traffic Alert</title></head><body>\n")
	outFileXML.write("<pre style=font: monospace>"+'\n')
	#outFileXML.write("<font size=\"9\" face=\"monospace\">"+'\n')
     	outFileXML.write("<h1>One NDS - Trigger Traffic Alert</h1>\n") 
     	outFileXML.write("<h4>Date/Time      :"+timeStamp1+"</h4>\n") 

def printReportTailXML():
	outFileXML.write("<hr>\n")
	outFileXML.write("</body></html>\n")

def getCurrentTime():
        currentTime=datetime.datetime.today().strftime('%Y%m%d_%H%M%s')
        return currentTime

class hostEntry:
   def __init__(self,inString):
       splitString = inString.split()
       self.site=splitString[1][3:5].lower()
       self.hostName=splitString[1].lower()
       self.hostIP=splitString[0]
       self.nodeType=splitString[1][0:3].lower()


class fileEntry:
      def __init__(self,inString):
        fmt_startTime = '%Y_%m_%d-%H_%M_%S'
        fmt_endTime = '%Y-%m-%d %H:%M:%S'
        splitString = inString.split()
        self.fileName=splitString[8]
        self.fileStartTime=datetime.strptime(splitString[8][18:37],fmt_startTime)-timedelta(seconds=int(300)*60)
        self.fileEndTime=datetime.strptime(splitString[5]+" "+splitString[6][:8], fmt_endTime)

class measCount:
      def __init__(self,inString):
        splitString = inString.split(',')
        self.nodeType=splitString[0].strip()
        self.nds9sp2adm=int(splitString[1].strip())
        self.nds9sp2netact=int(splitString[2].strip())
        self.nds16adm=int(splitString[3].strip())
        self.nds16netact=int(splitString[4].strip())
        self.nds17adm=int(splitString[5].strip())
        self.nds17netact=int(splitString[6].strip())

class PMMOResultEntry:
      def __init__(self):
        self.DN=""
        self.measurementType=""
        self.counterList=[]

class attribute:
        counterName=""
        counterValue=""

def getPmDataFromAdm():
     global sites
     global filteredFileList
     global nodeType
     global filesAvailable
     appLog.info("Entering getPmDataFromAdm()")
     #sites=['Dallas','Elgin','Nashville']
     sites=['da','el','nv']
     nodeType=["adm","pgw","pgd","sr1","sr2","sr3","sr4","bas","dev","pcs","cbe"]

     filesAvailable=False
     totalFileList=get_filepaths(baseDirectory+"data/")
     filteredFileList = [ x for x in totalFileList if timeStamp in x and admName in x] 
     if len(filteredFileList) ==0 :
        appLog.info("There are no files matching the adm and timestamp under data folder. Fetching the files from ADM...")
        status,result=commands.getstatusoutput("ssh -q -i /var/log/nsncare/KEYS/id-cntdb-dbm-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no dbmrun@"+admName+" ls -d -1 /opt/esymac/extras/esymacstarter/gmoTemp/pm/PM.*")
        fileList =result.rstrip().split('\n')
        filesToFetch = [ x for x in fileList if timeStamp in x]
        if len(filesToFetch) != 0 :
           filesAvailable=True
           for f in filesToFetch:
             appLog.info("Fetching the file .."+ f)
             os.system("scp -q -q -i /var/log/nsncare/KEYS/id-cntdb-dbm-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no dbmrun@"+admName+":"+f+" "+baseDirectory+"data/"+admName+"."+f.split("/")[-1])
             #os.system("scp -q root@"+admName+":"+f+" "+baseDirectory+"data/"+admName+"."+f.split("/")[-1])
           totalFileList=get_filepaths(baseDirectory+"data/")
           filteredFileList = [ x for x in totalFileList if timeStamp in x and admName in x]
           appLog.info("Number of files fetched .."+ str(len(filteredFileList)))
        else:
           appLog.info("There are no files matching the admname and timestamp in the ADM. Please retry with the different admname and or different timestamp")
           filesAvailable=False
     else:
           filesAvailable=True
 

def converXmlToObjects():
     appLog.info("Entering converXmlToObjects()")
     appLog.info( "----------------------------------------------------------")
     appLog.info("List of Files Processed")
     appLog.info("----------------------------------------------------------")
     global PMMOList
     PMMOList = []

     for fileName in filteredFileList:
       appLog.info("Procesing ..."+ fileName)
       if fileName.endswith(".gz"):
          os.system("gunzip "+ fileName)
       tree=ET.parse(fileName.replace(".gz",""))
       root = tree.getroot()
       for child in root:
          for pmmoResult in child.findall('PMMOResult'):
                tmpObject=PMMOResultEntry()
                tmpObject.counterList=[]
                for entry in pmmoResult:
                  if entry.tag=="MO":
                    for entry1 in entry:
                      tmpObject.DN=entry1.text.lower()
                  if entry.tag=="PMTarget":
                     tmpObject.measurementType = entry.attrib['measurementType']
                     for entry1 in entry:
                        tmpPair = attribute()
                        tmpPair.counterName = entry1.tag.strip()
                        tmpPair.counterValue= entry1.text.strip()
                        tmpObject.counterList.append(tmpPair)
                PMMOList.append(tmpObject)      
     appLog.info("The number of entries in PMMO List: "+ str(len(PMMOList)))
     
def processPmData():
     appLog.info("Entering processPmData()")
     appLog.info("filesAvailable: "+str(filesAvailable))
     hostListAll= [ hostEntry(line) for line in open(baseDirectory+"conf/ndsNodes1.txt",'r') if (line != '\n') and (line.startswith("#")!= 1)]
     if (nodeName != "all") and (filesAvailable==True):
        appLog.info( "----------------------------------------------------------")
        appLog.info( "Measurement List for the node :" + nodeName)
        appLog.info( "----------------------------------------------------------")
        appLog.info( "HostName".ljust(65)+ "MeasuremenType".ljust(20)+"TotalNoCounters".ljust(10))
        tempPrintList=[]
        filteredList = [ x for x in PMMOList if nodeName.lower() in x.DN]
        for x in filteredList:
          tempPrintList.append( x.DN.ljust(65)+x.measurementType.ljust(20)+ str(len(x.counterList)).ljust(10))
        tempPrintList.sort()
        for x in tempPrintList: appLog.info(x)

     if (nodeName == "all") and (filesAvailable==True):
          totalNumberOfServers=0
          totalNumberOfOK=0
          totalNumberOfNOK=0

          errorList=[]
     
          appLog.info("----------------------------------------------------------")
          appLog.info("Measurement List")
          appLog.info("----------------------------------------------------------")
          appLog.info( " ")

          for site in sites:
            for node in nodeType:
               appLog.info( "HostName".ljust(25)+ "TotalNoOfMeasurements".ljust(25)+"TotalNoCounters".ljust(25)+"NDS17".ljust(10)+"Status("+release+")".ljust(10))
               hostList = [x for x in hostListAll if x.hostName.lower().startswith(node) and x.site.lower()==site.lower()]
               hostList.sort(key=lambda x:int(x.hostName[-3]))
               #hostFile.sort()
               for a in hostList:
                 filteredList = [ x for x in PMMOList if a.hostName in x.DN]
                 totalCount=0
                 for y in filteredList: totalCount = totalCount + len(y.counterList)
                 validationString = ""

                 expectedCounters_nds9sp2 =  next((int(x.nds9sp2adm) for x in measCountList if x.nodeType==node),999)
                 expectedCounters_nds16 =  next((int(x.nds16adm) for x in measCountList if x.nodeType==node),999)
                 expectedCounters_nds17 =  next((int(x.nds17adm) for x in measCountList if x.nodeType==node),999)
                        
                 if release=="nds9sp2" :
                    expectedCounters = expectedCounters_nds9sp2
                 elif release=="nds16":
                    expectedCounters = expectedCounters_nds16
                 elif release=="nds17":
                    expectedCounters = expectedCounters_nds17

                 if totalCount==expectedCounters :
                    validationString = "OK"
                    totalNumberOfOK=totalNumberOfOK+1
                    totalNumberOfServers=totalNumberOfServers+1
                 else: 
                    validationString = "ERROR"
                    totalNumberOfNOK=totalNumberOfNOK+1
                    totalNumberOfServers=totalNumberOfServers+1
                 appLog.info( a.hostName.ljust(25)+ str(len(filteredList)).ljust(25)+str(totalCount).ljust(25)+str(expectedCounters_nds17).ljust(10)+validationString.ljust(10))
                 if validationString == "ERROR":
                   errorList.append(a.hostName.ljust(25)+ str(len(filteredList)).ljust(25)+str(totalCount).ljust(25)+str(expectedCounters_nds17).ljust(10)+validationString.ljust(10))
               appLog.info(" ")
            appLog.info( " ")

          
          if totalNumberOfNOK > 0:
            appLog.info("----------------------------------------------------------")
            appLog.info("Printing the Error List:")
            appLog.info("----------------------------------------------------------")
            appLog.info( "HostName".ljust(25)+ "TotalNoOfMeasurements".ljust(25)+"TotalNoCounters".ljust(25)+"NDS17".ljust(10)+"Status("+release+")".ljust(10))
            for x in errorList: appLog.info(x)
 
	
def emailReportNew(emailbody, emailAttachement):
        #Emailing the Report
        #tarFileName=baseDirectory+"reports/"+"zabbixCongAuditReport.2019_03_07T16_47_33.tar.gz"
        if config["email"]["enabled"]==True :
          if os.path.exists(emailAttachement) and os.path.exists(emailbody):
                #SCP the file to mail Server
                appLog.info("The attachement file is :"+os.path.basename(emailAttachement))
                appLog.info("Transferring the file :"+emailAttachement +" to the mail Server")
                command4="scp -q -i /var/log/nsncare/KEYS/id-sam-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no "+emailAttachement+" "+config["email"]["mailUser"]+"@"+config["email"]["mailServer"]+":"+config["email"]["mailDestDir"]+os.path.basename(emailAttachement)
                appLog.info(command4)
                status,inStr=commands.getstatusoutput(command4)

                #SCP the report file to mail server
                appLog.info("The body of the email is :"+os.path.basename(emailbody))
                appLog.info("Transferring the file :"+emailbody +" to the mail Server")
                command4a="scp -q -i /var/log/nsncare/KEYS/id-sam-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no "+emailbody+" "+config["email"]["mailUser"]+"@"+config["email"]["mailServer"]+":"+config["email"]["mailDestDir"]+os.path.basename(emailbody)
                appLog.info(command4a)
                status,inStr=commands.getstatusoutput(command4a)

                #Preparing the configuration file for email
                mailConfigYaml=baseDirectory+"conf/pythonMailConfig.yaml"
                with open(mailConfigYaml,"w")  as f:
                  f.write("From : "+ config["email"]["senderName"]+" <"+config["email"]["senderEmail"]+">\n")
                  f.write("To:\n")
                  for e in config["email"]["emailAddress"]:
                        f.write("  - "+e+"\n")
                  f.write("Subject: "+config["email"]["mailSubject"]+"-"+ timeStamp1+"\n")
                  f.write("message_type: html\n")
                  f.write("emailBody: "+config["email"]["mailDestDir"]+os.path.basename(emailbody)+"\n")
                  f.write("Attachements: \n")
                  f.write("  - "+config["email"]["mailDestDir"]+os.path.basename(emailAttachement)+"\n")

                #SCP the email Configuration file to mail server
                appLog.info("The email configuration file is :"+os.path.basename(mailConfigYaml))
                appLog.info("Transferring the file :"+mailConfigYaml +" to the mail Server")
                command4b="scp -q -i /var/log/nsncare/KEYS/id-sam-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no "+mailConfigYaml+" "+config["email"]["mailUser"]+"@"+config["email"]["mailServer"]+":"+config["email"]["mailDestDir"]+os.path.basename(mailConfigYaml)
                appLog.info(command4b)
                status,inStr=commands.getstatusoutput(command4b)

                #Send a command to mail server to email the report
                command5="ssh -q -i /var/log/nsncare/KEYS/id-sam-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no "+config["email"]["mailUser"]+"@"+config["email"]["mailServer"]+" \"/home/nsncare/cntdblogs/CLOUD/scripts/pythonMail.py -f "+config["email"]["mailDestDir"]+os.path.basename(mailConfigYaml)+"\""
                appLog.info(command5)
                status,inStr=commands.getstatusoutput(command5)
                time.sleep(2)

                #Remove the files
                command6="ssh -q -i /var/log/nsncare/KEYS/id-sam-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no "+config["email"]["mailUser"]+"@"+config["email"]["mailServer"]+" "+ "\"/usr/bin/rm -f "+ config["email"]["mailDestDir"]+os.path.basename(emailAttachement)+"\" 1>/dev/null 2>&1"
                appLog.info(command6)
                status,inStr=commands.getstatusoutput(command6)
                command7="ssh -q -i /var/log/nsncare/KEYS/id-sam-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no "+config["email"]["mailUser"]+"@"+config["email"]["mailServer"]+" "+ "\"/usr/bin/rm -f "+ config["email"]["mailDestDir"]+os.path.basename(emailbody)+"\" 1>/dev/null 2>&1"
                appLog.info(command7)
                status,inStr=commands.getstatusoutput(command7)

                command8="ssh -q -i /var/log/nsncare/KEYS/id-sam-rsa -o ConnectTimeout=10 -o BatchMode=yes -o StrictHostKeyChecking=no "+config["email"]["mailUser"]+"@"+config["email"]["mailServer"]+" "+ "\"/usr/bin/rm -f "+ config["email"]["mailDestDir"]+os.path.basename(mailConfigYaml)+"\" 1>/dev/null 2>&1"
                appLog.info(command8)
                status,inStr=commands.getstatusoutput(command8)
          else:
                appLog.error("The file for emailBody or emailAttachment couldn't be found")


if __name__=="__main__":
	baseDirectory="/var/log/nsncare/oneNds/checkCountersinAdm/"
	fmt = '%Y_%m_%dT%H_%M_%S'
        timeStamp=datetime.now().strftime('%Y_%m_%dT%H_%M_%S')
        timeStamp1=datetime.now().strftime('%d/%m/%Y %H:%M')

    	# Loading Logging configuration.
    	logConfFile = baseDirectory+"conf/logging.conf"
	logging.config.fileConfig(logConfFile)
	appLog = logging.getLogger("checkCountersinAdm")
	appLog.info("***********************START*********************************")

        #Load the configuration from file
        with open(baseDirectory+'conf/checkCountersinAdm.yaml','r') as f: config = yaml.load(f,Loader=yaml.FullLoader)

	#Definng the Argument Parser
	parser = argparse.ArgumentParser(description='To Ananlyze if PM files exported by ADM contains all counters')
	requiredNamed = parser.add_argument_group('required named arguments')
	requiredNamed.add_argument("-a", "--adm",help="which ADM to check",required=True)
	requiredNamed.add_argument("-n", "--node",help="which nodes PM files",required=True)
	requiredNamed.add_argument("-t", "--timestamp",help="for what time to check (20160320.140201)",required=True)
	requiredNamed.add_argument("-r", "--release",help="Against which  release to check",required=True)
	args=parser.parse_args()

	#Checking if arguments are given or not.
	admName=args.adm if args.adm else "None"
	nodeName=args.node if args.node else "None"
	timeStamp=args.timestamp if args.timestamp else "None"
	release=args.release if args.release else "None"


	#Moving the files from Reports folder to Archives
	#command="mv "+baseDirectory+"reports/*.txt"+" "+baseDirectory+"archives/"
	#appLog.info("Moving the files from reports/ to archives/ before the start of proccessing")
        #appLog.info(command)
	#os.system(command)
	#command="rm -f "+baseDirectory+"reports/*.html"
        #appLog.info(command)
	#os.system(command)
	#command="rm -f "+baseDirectory+"reports/checkCountersinAdm*"
        #appLog.info(command)
	#os.system(command)

	#Defining the report file
        reportName=baseDirectory+"reports/"+"checkCountersinAdm."+timeStamp+".txt"    
        reportFileHandle=open(reportName,"w")
        outFileNameXML=baseDirectory+"reports/"+"checkCountersinAdm."+timeStamp+".html"    
        outFileXML=open(outFileNameXML,"w")
        printReportHeaderXML()

        #Loading ndsNodeList
        measCountList= [ measCount(line) for line in open(baseDirectory+"conf/measurementCount.csv",'r') if (line != '\n') and (line.startswith("#")!= 1)]

	#Collecting Data from ADM
	getPmDataFromAdm()

	#Converting XML to objects
        converXmlToObjects()

	#Procss Data from ADM
	processPmData()

	#Closing the report file
	printReportTailXML()
	outFileXML.close()
        reportFileHandle.close()
      
        '''

	#Copying the hourly report from Reports folder to Archives
	command="cp "+baseDirectory+"reports/*.txt"+" "+baseDirectory+"archives/"
	appLog.info("Copying the hourly report from reports/ to archives/ ")
        appLog.info(command)
	os.system(command)

	#Compressing and storing the report files and data files together 
	reportsList=get_filepaths(baseDirectory+"reports/")
	tarFileName=baseDirectory+"reports/"+"checkTriggerTrafficReport."+datetime.now().strftime("%Y_%m_%dT%H_%M_%S")+".tar.gz"
	appLog.info("Tarred and Compressig reports files under "+ tarFileName)
	tar = tarfile.open(tarFileName, "w:gz")
	for name in reportsList: tar.add(name,arcname=os.path.basename(name))
	tar.close()

	#Emailing the Report
        if faultFound==True:
	  emailReportNew(outFileNameXML,tarFileName)
	#emailReportNew(outFileNameXML,tarFileName)
	
	#Performing Housekeeping
	cleanOldFiles(baseDirectory+"archives/", 10)
	for f in reportsList:
		appLog.info("Removing the file: "+ f)
		os.remove(f) 
	'''
