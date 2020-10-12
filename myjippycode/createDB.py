from openpyxl import load_workbook
from openpyxl import Workbook
import os
from collections import defaultdict
import collections
import csv
import PyPDF2
from downloadPDFs import downloadPDFs
#from manipulatePDFs import manipulatePdfs
#from outputData import outputData
import re
#import shutil

#THE NUMBER IS 38

def createDBs(listOfColleges, year, semester):
    #print ('hello')
    _semester = '4'
    if semester == "Fall":
        _semester = '3'
    elif semester == "Summer":
        _semester = '2'
    elif semester == "Spring":
        _semester = '1'
    else:
        print("I did a don goof")
    
    
    for college in listOfColleges:
        location = str(semester)+str(year)+'/'+'grd'+str(year)+_semester+str(college)
        try:
            pdfFileObj = open(str(semester)+str(year)+'/'+'grd'+str(year)+_semester+str(college)+'.pdf', 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
            pages = pdfReader.numPages
        except:
            print("PDFReader exception caught: " + str(semester)+str(year)+'/'+'grd'+str(year)+_semester+str(college)+'.pdf')
            continue
        
        #print('Lots of writing, this is gonna take a bit')
        
        textFileName = 'DIRTY_'+str(college)+str(semester)+str(year)+'.txt'
        textFileObj = open(textFileName, 'w')
        for page in range(0, pages):
        #for page in range(0, 1):
            #print('Current Page: ' + str(page) + ' out of ' + str(pdfReader.numPages-1))
            currentPage = pdfReader.getPage(page)
            #write command here
            textFileObj.write(currentPage.extractText())

            page+=1
        
        textFileObj.close()    
        #mainDirectory = os.getcwd() 
        #os.chdir(mainDirectory)
        
        #print ("On TextFile: " + textFileName)
        
        cleanTextFileName = 'CLEAN_'+str(college)+str(semester)+str(year)
        if os.path.exists(cleanTextFileName + '.txt'):
            os.remove(cleanTextFileName + '.txt')
        if os.path.exists(cleanTextFileName + '.csv'):
            os.remove(cleanTextFileName + '.csv')
        cleanFile = open(cleanTextFileName + '.txt', 'x')
        cleanFile.close()
        
        cleanFile = open(cleanTextFileName + '.txt', 'r+')
        dirtyFile = open(textFileName, 'r')
        #dirtyFile = _dirtyFile.readlines()
        
        cleanFile.write('section, A, A%, B, B%, C, C%, D, D%, F, F%, A-F total, GPA, I, S, U, Q, X, Total, Professor')
        
        writing_bool = False
        counter = 0
        line_number = 0
        for line in dirtyFile:
            if line_number < counter:
                new_line = line.replace('\r', '')
                newer_line = new_line.replace('\n', ',') #delineating characters 
                cleanFile.write(newer_line)
                line_number += 1
                continue
            #if "DEPARTMENT TOTAL:" in line:
            #    writing_bool = False
            #    counter += 19
            #    line_number += 1
            #if "COURSE TOTAL:" in line:
            #    writing_bool = False
            #    line_number += 1
            #    counter += 18
            if re.search("\w{4}-\d{3}-\d{3}", line):
                cleanFile.write('\n')
                new_line = line.replace('\r', '')
                newer_line = new_line.replace('\n', ',') #delineating characters 
                cleanFile.write(newer_line)
                line_number += 1
                counter += 20
            #if writing_bool == True:
            #    new_line = line.replace('\r', '')
            #    newer_line = new_line.replace('\n', ',') #delineating characters 
            #    cleanFile.write(newer_line)
            #    line_number += 1
            #    counter += 1
            #if "SECTION" in line:
            #    writing_bool = False
            #    line_number += 1
            #    counter += 1
            #if "Undergraduate" in line or "Graduate" in line:
            #    cleanFile.write('\n')
            #    writing_bool = True
            #    line_number += 1
            #   counter += 1
        dirtyFile.close()
        cleanFile.close()
           
        #os.remove(textFileName + '.txt') #comment this line to keep dirty file info
        
        no_csv = cleanTextFileName + '.txt'
        CSV_file = os.path.splitext(no_csv)[0]
        os.rename(no_csv, CSV_file + '.csv')
        
        if os.path.exists('formatted_' + cleanTextFileName + '.csv'):
            os.remove('formatted_' + cleanTextFileName + '.csv')
        formattedFile = open('formatted_' + cleanTextFileName + '.csv', 'x')
        formattedFile.close()
        
        formattedFile = open('formatted_' + cleanTextFileName + '.csv', 'r+')
        formattingFile = open(cleanTextFileName + '.csv', 'r')
        for line in formattingFile:
            if not re.match(r'^\s*$', line):
                formattedFile.write(line)
                
        formattedFile.close()
        formattingFile.close()
        #os.remove(cleanTextFileName + 'csv') #comment this line to keep cleaned csv that isnt yet formatted
        
        #os.rename(os.getcwd() +  '/' + cleanTextFileName + '.csv', os.getcwd() + '/' + cleanTextFileName + '.csv/' + str(semester) + str(year))
        
        #otherOutputDirectory = os.getcwd() + '/' + str(semester) + str(year) + '/' + 'PDF_Files'
        #if not os.path.exists(otherOutputDirectory):
        #    os.makedirs(otherOutputDirectory)
    
        #print('Cleaning!')
            
        outputDirectory = os.getcwd() + '/' + str(semester) + str(year) + '/' + 'CSV_Files' + college
        if not os.path.exists(outputDirectory):
            os.makedirs(outputDirectory)
        
        path_current = str(os.getcwd()) + '/'
        path_plus_csv_folder = path_current + str(semester) + str(year) + '/' + 'CSV_Files' + college + '/'
       
        os.rename(path_current + cleanTextFileName + '.csv', path_plus_csv_folder + cleanTextFileName + '.csv')
        os.rename(path_current + 'formatted_' + cleanTextFileName + '.csv', path_plus_csv_folder + 'formatted_' + cleanTextFileName + '.csv')
        os.rename(path_current + textFileName, path_plus_csv_folder + textFileName)
         
        #os.remove(path_current + cleanTextFileName + '.csv')
        #os.remove(path_current + 'formatted_' + cleanTextFileName + '.csv')
        #os.remove(path_current + textFileName)
    
    #for college in listOfColleges:
    ###This isnt playing nice and I have Absolutely no idea why, so PDF's are staying poorly formatted and I just might delete them###
    #    path_pdf_current = str(os.getcwd()) + '/' + str(semester) + str(year) + '/'
    #    path_plus_pdf_folder = path_pdf_current + 'PDF_Files' + '/'  
    #    pdf_shortcut = 'grd' + str(year) + _semester + str(college) + '.pdf'    
     #   os.rename(path_pdf_current + pdf_shortcut, path_plus_pdf_folder + pdf_shortcut)