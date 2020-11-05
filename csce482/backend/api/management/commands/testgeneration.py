from api.models import Course
from api.models import Professor
from api.models import Course_Prof
from api.models import Activity
from api.models import Section
from api.models import Schedule
from api.models import Activity_Instance
from users.models import User

from django.core.management import base

import random
import string
import names #pip install names
import math
from datetime import datetime
from datetime import time
from datetime import timedelta

NUMBER_OF_PROFS = 10
NUMBER_OF_ACTIVITIES = 20
MAX_NUMBER_OF_SECTIONS = NUMBER_OF_ACTIVITIES
NUMBER_OF_ACTIVITIES_PER_INSTANCE = 2
NUMBER_OF_SCHEDULES = 1

courses = []
profs = []
activities = []
activities_classtype = [False for i in range(20)]
act_insts = []
schedules = []
#prof_plus_dept = []
course_profs = []
sections = []

users = [User.objects.first()]

list_of_depts = [
    "CHEM",
    "ENGL",
    "ENGR",
    "MATH",
    "PHYS",
    "CSCE",
    "COMM",
    "STAT"
]

list_of_buildings = [
    "EABC",
    "BLOC",
    "HRBB",
    "ZACH"
]

list_of_locations = [
    "EABC",
    "BLOC",
    "HRBB",
    "ZACH",
    "ONLINE",
    "CHEM",
    "PHYS"
]

list_of_terms = [
    "FALL" + " " + str(datetime.now().year),
    "SPRING" + " " + str(datetime.now().year),
    "SUMMER" + " " + str(datetime.now().year)
]

list_of_days = [
    "MON",
    "TUES",
    "WED",
    "THURS",
    "FRI"
]

list_of_starttimes = [
    datetime(2020, 1, 1, 8, 0, 0),
    datetime(2020, 1, 1, 9, 10, 0),
    datetime(2020, 1, 1, 10, 20, 0),
    datetime(2020, 1, 1, 11, 30, 0),
    datetime(2020, 1, 1, 12, 40, 0),
    datetime(2020, 1, 1, 13, 50, 0),
    datetime(2020, 1, 1, 15, 0, 0),
    datetime(2020, 1, 1, 9, 35, 0),
    datetime(2020, 1, 1, 11, 10, 0),
    datetime(2020, 1, 1, 12, 55, 0),
    datetime(2020, 1, 1, 14, 45, 0),
    datetime(2020, 1, 1, 16, 25, 0),
    datetime(2020, 1, 1, 18, 5, 0)
]

list_of_offices = []
for k in range(NUMBER_OF_PROFS):
    list_of_offices.append(list_of_buildings[random.randint(0,len(list_of_buildings)-1)] + " " + str(random.randint(100, 699)))
    
prof_names = []
for j in range(NUMBER_OF_PROFS):
    prof_names.append(names.get_full_name())
    
list_of_sections = []
for i in range(MAX_NUMBER_OF_SECTIONS):
    list_of_sections.append(str(random.randint(101, 499)))

def generate_random_course_objs(MAX_NUMBER_OF_SECTIONS, list_of_depts):
    for element in range(MAX_NUMBER_OF_SECTIONS):
        _course_id = list_of_depts[random.randint(0,len(list_of_depts)-1)] + " " + list_of_sections[random.randint(0,len(list_of_sections)-1)]
        if _course_id[5] == "4":
            _title = "Complex " + "".join([random.choice(string.ascii_letters) for i in range(15)])
        elif _course_id[5] == "3":
            _title = "Moderate " + "".join([random.choice(string.ascii_letters) for i in range(15)])
        elif _course_id[5] == "2":
            _title = "Beginner " + "".join([random.choice(string.ascii_letters) for i in range(15)])
        elif _course_id[5] == "2":
            _title = "Intro " + "".join([random.choice(string.ascii_letters) for i in range(15)])
        else:
            _title = "Something broke"
        
        new_course, created = Course.objects.get_or_create(
            course_id = _course_id
        )
        if created:
            new_course.title = _title
        courses.append(new_course)
        new_course.save()
        #print("course created: " + _course_id) #DEBUG

def generate_random_prof_objs(NUMBER_OF_PROFS, prof_names, list_of_depts, list_of_offices):
    for element in range(NUMBER_OF_PROFS):
        new_prof = Professor.objects.get_or_create(
            name = prof_names[element],
            dept = list_of_depts[random.randint(0,len(list_of_depts)-1)],
            office = list_of_offices[element]
        )[0]

        profs.append(new_prof)
        new_prof.save()
        #prof_plus_dept.append(name, dept)
        
def generate_random_course_prof_objs(MAX_NUMBER_OF_SECTIONS, courses, profs):        
    for element in range(len(courses)):
        _course = courses[element]
        _professor = profs[random.randint(0,len(profs)-1)] 
            
        A = random.uniform(0,10)
        B = random.uniform(0,10)
        C = random.uniform(0,10)
        D = random.uniform(0,10)
        F = random.uniform(0,10)
        Q = random.uniform(0,10)
            
        _sum = A+B+C+D+F+Q
            
        _A= A/_sum
        _B= B/_sum
        _C= C/_sum
        _D= D/_sum
        _F= F/_sum
        _Q= Q/_sum
            
        _percent_A = _A*100
        _percent_B = _B*100
        _percent_C = _C*100
        _percent_D = _D*100
        _percent_F = _F*100
        _percent_Q = _Q*100
        
        new_course_prof, created = Course_Prof.objects.get_or_create(
            course = _course,
            professor = _professor
        )
        if created:
            new_course_prof.percent_A = _percent_A
            new_course_prof.percent_B = _percent_B
            new_course_prof.percent_C = _percent_C
            new_course_prof.percent_D = _percent_D
            new_course_prof.percent_F = _percent_F
            new_course_prof.percent_Q = _percent_Q
        new_course_prof.save()
        course_profs.append(new_course_prof)
        #print('course_prof created for ' + _course.course_id) #DEBUG

def generate_random_activity_objs(NUMBER_OF_ACTIVITIES, list_of_terms, courses):
    for element in range(NUMBER_OF_ACTIVITIES):
        if random.randint(0,1) == 1: #non class event
            _title = "".join([random.choice(string.ascii_letters) for i in range(15)])
            _term = list_of_terms[0]
            new_activity = Activity.objects.get_or_create(
                title = _title,
                term = _term
            )[0]
            activities.append(new_activity)
            new_activity.save()
        else: #class event
            _title = courses[element].course_id + "-" + list_of_sections[element]
            #print("title is " + _title) #DEBUG
            _term = list_of_terms[0]
            activities_classtype[element] = True            
            new_activity, created = Activity.objects.get_or_create(
                title = _title,
                term = _term
            )
            activities.append(new_activity)
            new_activity.save()

            if created:
                _course_prof = Course_Prof.objects.all().filter(
                    course_id__exact = courses[element].course_id
                ).first()
                #if _course_prof == None: #DEBUG
                    #print("element = " + str(element)) #DEBUG
                    #print("course_prof is None") #DEBUG

                _honors = random.randint(0,1)
                if _honors == 0:
                    _honors = False
                else:
                    _honors = True
                
                _section_num = int(list_of_sections[element])
                _crn = random.randint(500, 599)
                _credit_hours = random.randint(1,4)
                _total_seats = random.randint(10, 100)
                new_section = Section.objects.create(
                    activity = new_activity,
                    course_prof = _course_prof,
                    term = _term,
                    honors = _honors,
                    section_num = _section_num,
                    crn = _crn,
                    credit_hours = _credit_hours,
                    total_seats = _total_seats
                )
                sections.append(new_section)
                new_section.save()
        
def generate_random_act_inst_objs(NUMBER_OF_ACTIVITIES, NUMBER_OF_ACTIVITIES_PER_INSTANCE, activities, list_of_locations, list_of_days, list_of_starttimes):
    for element in range(len(activities)):
        iterator = random.randint(0,len(list_of_starttimes)-1)
        for item in range(NUMBER_OF_ACTIVITIES_PER_INSTANCE):
            #print("instance#: " + str(item)) #DEBUG
            _activity = activities[element]
            _location = list_of_locations[random.randint(0,len(list_of_locations)-1)]
            if item == 0:
                _day = list_of_days[random.randint(0,len(list_of_days)-4)]
            else:
                _day = list_of_days[random.randint(len(list_of_days)-3, len(list_of_days)-1)]
            _starttime = list_of_starttimes[iterator]
            #print(_starttime) #DEBUG
            if iterator <= len(list_of_starttimes)/2:
                #raw_time_conversion = int(_starttime[0])*10*60+int(_starttime[1])*60+int(_starttime[3])*10+int(_starttime[4])
                #raw_time_conversion = raw_time_conversion + 50
                
                #time0 = raw_time_conversion
                #time1 = raw_time_conversion-time0
                #time3 = raw_time_conversion-time0-time1
                #time4 = raw_time_conversion-time0-time1-time3 
                
                #time0 = math.floor(time0/600)
                #time1 = math.floor(time1/60)
                #time3 = math.floor(time3/10)
                #time4 = math.floor(time4)
                    
                #time_conversion = str(time0)+str(time1)+":"+str(time3)+str(time4)+":00"
                _endtime = _starttime + timedelta(minutes=50)
            else:
                #raw_time_conversion = int(_starttime[0])*10*60+int(_starttime[1])*60+int(_starttime[3])*10+int(_starttime[4])
                #raw_time_conversion = raw_time_conversion + 75
                    
                #time0 = raw_time_conversion
                #time1 = raw_time_conversion-time0
                #time3 = raw_time_conversion-time0-time1
                #time4 = raw_time_conversion-time0-time1-time3 
                
                #time0 = math.floor(time0/600)
                #time1 = math.floor(time1/60)
                #time3 = math.floor(time3/10)
                #time4 = math.floor(time4)
                    
                #time_conversion = str(time0)+str(time1)+":"+str(time3)+str(time4)+":00"
                _endtime = _starttime + timedelta(hours=1, minutes=15)
            
            new_activity_instance = Activity_Instance.objects.get_or_create(
                activity = _activity,
                location = _location,
                day      = _day,
                starttime= _starttime,
                endtime  = _endtime
            )[0]
            act_insts.append(new_activity_instance)
            new_activity_instance.save()
            
class Command(base.BaseCommand): 
    def handle(self, *args, **options):
        print("generate_random_course_objs starting")
        generate_random_course_objs(MAX_NUMBER_OF_SECTIONS, list_of_depts)
        print("generate_random_prof_objs starting")
        generate_random_prof_objs(NUMBER_OF_PROFS, prof_names, list_of_depts, list_of_offices)
        print("generate_random_course_prof_objs starting")
        generate_random_course_prof_objs(MAX_NUMBER_OF_SECTIONS, courses, profs)
        print("generate_random_activity_objs starting")
        generate_random_activity_objs(NUMBER_OF_ACTIVITIES, list_of_terms, courses)
        print("generate_random_act_inst_objs starting")
        generate_random_act_inst_objs(NUMBER_OF_ACTIVITIES, NUMBER_OF_ACTIVITIES_PER_INSTANCE, activities, list_of_locations, list_of_days, list_of_starttimes)
        print("finished generating")