import requests
import json
import math

import sys

from django.apps import apps
from django.conf import settings
from django.core.management import base

from api.models import Professor

class RateMyProfScraper:

    def __init__(self,schoolid):
        self.UniversityId = schoolid
        self.professorlist = self.createprofessorlist()
        self.indexnumber = False

    def createprofessorlist(self):#creates List object that include basic information on all Professors from the IDed University
        tempprofessorlist = []
        num_of_prof = self.GetNumOfProfessors(self.UniversityId)
        num_of_pages = math.ceil(num_of_prof / 20)
        i = 1
        while (i <= num_of_pages):# the loop insert all professor into list
            string = "http://www.ratemyprofessors.com/filter/professor/?&page=" + str(
                i) + "&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                self.UniversityId)
            page = requests.get(string)
            temp_jsonpage = json.loads(page.content)
            temp_list = temp_jsonpage['professors']
            tempprofessorlist.extend(temp_list)
            i += 1
        return tempprofessorlist

    def GetNumOfProfessors(self,id):  # function returns the number of professors in the university of the given ID.
        page = requests.get(
            "http://www.ratemyprofessors.com/filter/professor/?&page=1&filter=teacherlastname_sort_s+asc&query=*%3A*&queryoption=TEACHER&queryBy=schoolId&sid=" + str(
                id))  # get request for page
        temp_jsonpage = json.loads(page.content)
        num_of_prof = temp_jsonpage['remaining'] + 20  # get the number of professors
        return num_of_prof

    def SearchProfessor(self, ProfessorName):
        self.indexnumber = self.GetProfessorIndex(ProfessorName)
        self.PrintProfessorInfo()
        return self.indexnumber

    def GetProfessorIndex(self,ProfessorName):  # function searches for professor in list
        for i in range(0, len(self.professorlist)):
            if (ProfessorName == (self.professorlist[i]['tFname'] + " " + self.professorlist[i]['tLname'])):
                return i
        return False  # Return False is not found

    def PrintProfessorInfo(self):  # print search professor's name and RMP score
        if self.indexnumber == False:
            print("error")
        else:
            print(self.professorlist[self.indexnumber])

    def WriteProfessorDetails(self):  # print search professor's name and RMP score
        if self.indexnumber == False:
            print("error")
            return "error"
        else:
            RMP_link = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + str(self.professorlist[self.indexnumber]["tid"])
            print(str(self.professorlist[self.indexnumber]["overall_rating"]) + " " + str(self.professorlist[self.indexnumber]["rating_class"]) + " " + str(self.professorlist[self.indexnumber]["tNumRatings"]) + " " + str(RMP_link))
            
            #write to DB here
            
            #try:
            #    overwrite_prof = Professor.objects.get(
            #        name = str(self.professorlist[self.indexnumber]['tFname'] + " " + self.professorlist[self.indexnumber]['tLname'])
            #    )[0]
            #    
            #    overwrite_prof.overall_rating = str(self.professorlist[self.indexnumber]["overall_rating"])
            #    overwrite_prof.rating_class   = str(self.professorlist[self.indexnumber]["rating_class"])
            #    overwrite_prof.tNumRatings    = str(self.professorlist[self.indexnumber]["tNumRatings"])
            #    overwrite_prof.RMP_link       = str(RMP_link)
            #    
            #    overwrite_prof.save()
            #except:
            #    print("prof object get and/or prof write to db failed")

class Command(base.BaseCommand):
    def handle(self, *args, **options):
        professors = ["Charles Hall"] #access db for professor list
        #professors_queryset = Professor.objects.all() #for handling of actual professor objects instead of string
        #professors = list(professors_queryset) #this needs to be tested, unexpected behavior can happen but idk #for handling of actual professor objects instead of string
        TAMU = RateMyProfScraper(1003) #1003 is tamus code
        for professor in professors: 
            print("Scraping: " + professor)
            #print("Scraping: " + professor.name) #for handling of actual professor objects instead of string
            TAMU.SearchProfessor(professor)
            #TAMU.SearchProfessor(professor.name) #for handling of actual professor objects instead of string
            TAMU.WriteProfessorDetails()
