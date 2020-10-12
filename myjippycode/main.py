#from createMasterDB import createMasterDBs
from createDB import createDBs
from downloadPDFs import downloadPDFs
#from googleOCR import googleOCR
#from manipulatePDFs import manipulatePdfs
#from outputData import outputData
from openpyxl import Workbook
import os
from os import path
import datetime
import time
import math

from glob import glob

start = time.time()
_author_ = "Marcus Salinas"
_refiner_ = "Joshua Sass" #idk just felt right LOL


def find_ext(dr, ext):
    return glob(path.join(dr, "*.{}".format(ext)))


def getSemesterChar(semester):
    if semester == "Spring":
        return "A"
    elif semester == "Summer":
        return "B"
    elif semester == "Fall":
        return "C"
    else:
        return "N/A"

def semesterCharToURLChar(semesterChar):
    if semesterChar == "A":
        return "1"
    elif semesterChar == "B":
        return "2"
    elif semesterChar == "C":
        return "3"
    else:
        return "0"

# url = "http://web-as.tamu.edu/gradereport/PDFReports/"
url = "http://web-as.tamu.edu/gradereport/"
listOfColleges = [
    "AG",  # AGRICULTURE AND LIFE SCIENCES
    "AR",  # ARCHITECTURE
    "BA",  # BUSINESS
    "ED",  # EDUCATION Spring 2016
    #"EL",  # ENGLISH LANGUAGE INSTITUTE No access 3/16/2017
    "EN",  # ENGINEERING
    "GB",  # GEORGE BUSH SCHOOL OF GOVERNMENT
    "GE",  # GEOSCIENCES
    "LA",  # LIBERAL ARTS Spring 2014
    "MD", # MEDICINE No longer have access
    "MS",  # MILITARY SCIENCE
    "SC",  # SCIENCE
    "VM"  # VETERINARY MEDICINE
]

listOfSemesters = [
    "Spring",  # A
    "Summer",  # B
    "Fall"  # C
]

listOfYears = [ 
    str(datetime.datetime.now().year),
    str(datetime.datetime.now().year-1),
    str(datetime.datetime.now().year-2),
    str(datetime.datetime.now().year-3),
    str(datetime.datetime.now().year-4),
    str(datetime.datetime.now().year-5)
]
MainDirectory = os.getcwd()
outputDirectory = os.getcwd() + '/GradeDistributionsDB'
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

#testing
#print("god this code sucks")

for year in listOfYears:
    for semester in listOfSemesters:
        
        #this wont catch all, but itll catch most
        if semester == "Spring" and str(datetime.datetime.now().year) == year and datetime.datetime.now().month < 6: 
            continue #gradereport will not have this semester
        
        if semester == "Summer" and str(datetime.datetime.now().year) == year and datetime.datetime.now().month < 9:
            continue #gradereport will not have this semester
            
        if semester == "Fall" and str(datetime.datetime.now().year) == str(year) and datetime.datetime.now().month < 12: 
            continue #this statement never happens because gradereports are made available in late december, but in case that changes here is a blanket statement
            
        #print ("On Semester: " + semester)
        os.chdir(MainDirectory)
        semesterChar = getSemesterChar(semester)
        folderName = semester + str(year)
        
        pdfFileDirectory = os.getcwd() + "/GradeDistributionsDB/" + folderName
        yearAndURLChar = str(year) + semesterCharToURLChar(semesterChar)

        for x in range(0, len(listOfColleges)):
           #print("On College: " + str(listOfColleges[x]))
           downloadPDFs(url, str(year), semesterChar, listOfColleges[x])

        os.chdir(pdfFileDirectory)

        os.chdir(MainDirectory)
        os.chdir(outputDirectory)
            
        createDBs(listOfColleges, str(year), semester)
        
end = time.time()
print("Code Completed Successfully. Time Elapsed(minutes): " + str(math.trunc((end-start)/60)))
