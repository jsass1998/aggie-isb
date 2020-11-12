import sys
import asyncio
from html import unescape
import time
import datetime
import random
from itertools import groupby
from typing import List, Tuple
from django.core.management import base
from django.db import transaction
from api.banner_requests import BannerRequests
#from scraper.models import Course, Instructor, Section, Meeting, Department, Grades
from api import models as models
#from scraper.models.course import generate_course_id #"".join((dept, course_num, '-', term))
#from scraper.models.section import generate_meeting_id #"".join((section_id, meetings_count))
if sys.version_info[:2] >= (3, 7):
    from asyncio import get_running_loop
else:
    from asyncio import _get_running_loop as get_running_loop

from api.management.commands.utils.scraper_utils import (
    get_all_terms, get_recent_terms,
)

# Set of the courses' ID's

def generate_course_id(dept: str, course_num: str, term: str):
    return "".join((dept, course_num, '-', term))

def generate_meeting_id(section_id: str, meetings_count: str):
    return "".join((section_id, meetings_count))

def convert_meeting_time(string_time: str) -> datetime.time:
    """ Converts a meeting time from a string in format hhmm to datetime.time object.
        ex) 1245 = 12:45am. 1830 = 6:30 pm.
    """

    if not string_time:
        return None

    hour = int(string_time[0:2])
    minute = int(string_time[2:4])
    meeting_time = datetime.time(hour, minute)

    return meeting_time
    
def parse_meeting_days(meetings_data) -> List[bool]:
    """ Generates a list of seven booleans where each corresponds to a day in the week.
        The first is Monday and the last is Sunday. If true, there is class that day
    """
    meeting_class_days = [
        'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    return [meetings_data['meetingTime'][day] for day in meeting_class_days]

def get_department_names(terms: List[str]) -> List[Tuple[str,str,str,str]]:
    """ Queries database for list of all departments """
    
    f = open("departments.txt", "r")
    lines = f.readlines()
    
    depts = []
    
    for line in lines:
        string = line.strip()
        _dept = string.split()
        
        code_term = _dept[0]
        department = _dept[1]
        garbageimnotworriedabout = _dept[2]
        code = _dept[len(_dept)-1]
        
        dept = (code_term, department, garbageimnotworriedabout, code)
        #print(dept)
        
        depts.append(dept)
    
    #print("returning depts to home: " + str(len(depts)))
    return depts
    ###depts = (Department.objects.filter(term__in=terms).order_by('term')
    ###         .values('code', 'term'))
    #grouped = groupby(depts, key=lambda x: x['term'])

    #return ((dept['code'], term) for term, group in grouped for dept in group)
    
def parse_section(course_data) -> Tuple[models.Section, List[models.Activity]]: # pylint: disable=too-many-locals
    """ Puts section data in database & calls parse_meeting.
        Called from parse_course.
    """

    section_id = int(course_data['id'])
    subject = course_data['subject']
    course_number = course_data['courseNumber']
    section_number = course_data['sequenceNumber']
    term_code = course_data['term']

    crn = course_data['courseReferenceNumber']

    min_credits = course_data['creditHourLow']
    max_credits = course_data['creditHourHigh']
    max_enrollment = course_data['maximumEnrollment']
    current_enrollment = course_data['enrollment']
    # Go through section attributes to determine if the class is honors
    honors = False
    for attributes in course_data.get('sectionAttributes', []):
        if attributes['description'] == "Honors":
            honors = True
            break

    web = course_data.get('instructionalMethod', "") == "Web Based"

     
    try:
        _activity = models.Activity.objects.get_or_create(
            title = subject + str(course_number) + "-" + str(section_number),
            term = term_code
            )[0]
        _activity.save()
        #print("wrote new activity")
    except Exception as e:
        #print(str(e))
        return None
    if _activity:    
        try:
            for faculty_data in course_data['faculty']:
            # We only care about the primary instructor, so skip all of the other ones
                if not faculty_data['primaryIndicator']:
                    continue
                name = faculty_data.get("displayName")
                if name is None:
                    name = "TBD"
                    #print("name is TBD")

            _course = models.Course.objects.get_or_create(course_id = subject + str(course_number))[0]
            try:
                _prof = models.Professor.objects.get_or_create(name = name, dept = subject)[0]
            except:
                #print("prof failed")
                statement = 5
            _course_prof = models.Course_Prof.objects.get_or_create(
                course = _course,
                professor = _prof
            )[0]
            _course_prof.save()
            
            #print("wrote new course_prof")
        except Exception as e:
            #print(str(e))
            return None
    if _course_prof:    
        try:
            try:
                new_section_number = int(section_number)
                section_number = new_section_number
            except:
                new_section_number = section_number[1:2]
                section_number = new_section_number
            #try:
            #    term_desc = course_data['termDesc']
            #    term_array = term_desc.split()
            #    count_term = 0
            #    for term in term_array:
            #        count_term = count_term + 1
            #        if term == "-":
            #            campus = "" 
            #            for i in range(count_term, len(term_array)-2):
            #                campus = campus + term_array[count_term + 1]
            #except:
            #    campus = "No Campus"
                        
                        
            ###*** ADD CAMPUS FIELD TO SECTION MODEL WHEN MIGRATION COMPLETE ***###            
            _section = models.Section.objects.get_or_create(
                activity = _activity,
                course_prof = _course_prof,
                term = term_code,
                section_num = section_number,
                crn = crn,
                credit_hours = min_credits,
                honors = honors,
                web = web,
                total_seats = max_enrollment,
                seats_taken = current_enrollment
            )[0]
            _section.save()
            #print("wrote new section")
        except Exception as e:
            #print(str(e))
            return None
        
    ### MINOR ISSUES HERE  !!!!!! FIX FIX FIX
    #print("\r\n")
    #print(course_data)
    #print("\r\n")
    
    monday = False
    tuesday = False
    wednesday = False
    thursday = False
    friday = False
    
    if _section:
        for meetingData in course_data['meetingsFaculty']:
            monday = meetingData['meetingTime']['monday']
            tuesday = meetingData['meetingTime']['tuesday']
            wednesday = meetingData['meetingTime']['wednesday']
            thursday = meetingData['meetingTime']['thursday']
            friday = meetingData['meetingTime']['friday']
            
            _starttime = meetingData['meetingTime']['beginTime']
            _endtime = meetingData['meetingTime']['endTime']
            
            if _starttime is not None:
                start_time = convert_meeting_time(_starttime)
            else:
                start_time = convert_meeting_time('2000')
                
            if _endtime is not None:
                end_time = convert_meeting_time(_endtime)
            else:
                start_time = convert_meeting_time('2100')    
            
            
            building = meetingData['meetingTime']['building']
            
            if building is not None:
                building = unescape(building)
            else:
                building = "None"
            
        if monday:
            try:
                _activity_instance = models.Activity_Instance.objects.get_or_create(
                    activity = _activity,
                    location = building,
                    day = "monday",
                    starttime = start_time,
                    endtime = end_time
                )[0]
                _activity_instance.save()
                #print("wrote new monday")
            except Exception as e:
                #print(str(e))
                return None
        if tuesday:
            try:
                _activity_instance = models.Activity_Instance.objects.get_or_create(
                    activity = _activity,
                    location = building,
                    day = "tuesday",
                    starttime = start_time,
                    endtime = end_time
                )[0]
                _activity_instance.save()
                #print("wrote new tuesday")
            except Exception as e:
                #print(str(e))
                return None
                
        if wednesday:
            try:
                _activity_instance = models.Activity_Instance.objects.get_or_create(
                    activity = _activity,
                    location = building,
                    day = "wednesday",
                    starttime = start_time,
                    endtime = end_time
                )[0]
                _activity_instance.save()
                #print("wrote new weds")
            except Exception as e:
                #print(str(e))
                return None
        if thursday:
            try:
                _activity_instance = models.Activity_Instance.objects.get_or_create(
                    activity = _activity,
                    location = building,
                    day = "thursday",
                    starttime = start_time,
                    endtime = end_time
                )[0]
                _activity_instance.save()
                #print("wrote new thurs")
            except Exception as e:
                #print(str(e))
                return None
        if friday:
            try:
                _activity_instance = models.Activity_Instance.objects.get_or_create(
                    activity = _activity,
                    location = building,
                    day = "friday",
                    starttime = start_time,
                    endtime = end_time
                )[0]
                _activity_instance.save()
                #print("wrote new fri")
            except Exception as e:
                #print(str(e)) 
                return None
        if _section.web and not monday and not tuesday and not wednesday and not thursday and not friday:
            try:
                start_time = convert_meeting_time('2000')
                end_time = convert_meeting_time('2100')

                _activity_instance = models.Activity_Instance.objects.get_or_create(
                    activity = _activity,
                    location = "ONLINE",
                    day = "ONLINE",
                    starttime = start_time,
                    endtime = end_time
                )[0]
                _activity_instance.save()
                #print("wrote new web")
            except Exception as e:
                #print(str(e))
                return None
    return None
    
def parse_instructor(course_data, dept) -> models.Professor:
    """ Parses the instructor data and saves it as a Instructor model.
        Called from parse_course.
    """

    # Can have multiple instructor entries, although most will have 0-1
    for faculty_data in course_data['faculty']:
        # We only care about the primary instructor, so skip all of the other ones
        if not faculty_data['primaryIndicator']:
            continue

        name = faculty_data.get("displayName")

        if name is None:
            return None

        #email = faculty_data['emailAddress']

        #f = open("debug.txt", "a")
        #f.write(name)
        #f.close()
        
        new_name_array = name.split()
        #print(new_name_array)
        new_name_zero = new_name_array[0]
        new_name = new_name_array[len(new_name_array)-1] + " " + new_name_zero[0]
        #print(new_name)
        updated_name = new_name_array[0] + " " + new_name_array[len(new_name_array)-1]
        #print (updated_name)
        
        try:
            prof = models.Professor.objects.get(name=new_name, dept=dept)[0]
        except Exception as e:
            updated_prof = models.Professor.objects.get_or_create(
                name = updated_name,
                dept = dept,
                office = ""
            )[0]
            updated_prof.save()
            #print("wrote new prof")
            return updated_prof
        try:
            updated_prof = models.Professor.objects.get_or_create(
                name = updated_name,
                dept = dept,
                office = ""
            )[0]
            prof.delete()
            prof.save()
            updated_prof.save()
            #print("wrote to prof")
            
            #check = models.Professor.objects.get_or_create(name = updated_name)[0]
            #if check:
            #    print("true: " + check.name)
            #else:
            #    print("false: " + prof.name)
            #return updated_prof
        except Exception as e:
            #print(str(e))
            statement = 5


    return None  #I DO NOT KNOW WHAT TO RETURN HERE. FUTURE JOSH PROBLEM :)  
    
def parse_course(course_data: List,
                 courses_set: set,
                 instructors_set: set,
                ) -> Tuple[models.Course, models.Professor, Tuple[models.Section, List[models.Activity]]]:
    """ Creates Course model and saves it to the databsae.
        Calls parse_instructor and parse_section
    """
    #print(course_data)
    
    dept = course_data['subject']
    course_number = course_data['courseNumber']
    term_code = course_data['term']

    # Generate the course's id using the above data
    course_id = generate_course_id(dept, course_number, term_code)

    # Some course titles contain escaped characters(ex. &amp;), so unescape them
    title = unescape(course_data['courseTitle'])
    # Some titles also start with "HNR-" if the first sections is honors, remove it
    if title[0:4] == "HNR-":
        title = title[4:]
    credit_hours = course_data['creditHourLow']

    # Parse the instructor, then send the returned Instructor model to parse_section
    instructor_model = parse_instructor(course_data, dept)
    section_data = parse_section(course_data)
    #print("parsing a section")

    if instructor_model is not None and instructor_model not in instructors_set:
        instructors_set.add(instructor_model)
    else:
        # Set it to None so that it doesn't get added to the list of instructors to save
        instructor_model = None

    return (None, instructor_model, section_data)    

def parse_all_courses(course_list, term: str, courses_set: set,
                      instructors_set: set) -> List:
    """ Helper function that's passed to banner.search so we can download the dept data
        and parse it on one thread.
    """
    #print("parse all course begin")
    #f = open("debug.txt", "a")
    #f.write("parse all course begin")
    #f.close()
    
    dept_name = course_list[0].get('subject', '') if course_list else ''

    random.shuffle(course_list)
    
    #print(course_list)
    time.sleep(5)
    for course in course_list:
        time.sleep(1)
        parse_course(course, courses_set, instructors_set) 
    
    print(f'{dept_name} {term}: Scraped {len(course_list)} sections')
    return None
    
def get_course_data(  # pylint: disable=too-many-locals
        depts_terms,
) -> Tuple[List[models.Professor], List[models.Section], List[models.Activity_Instance], List[models.Course]]:
    """ Retrieves all of the course data from Banner """
    # This limit is artifical for speed at this point,
    concurrent_limit = 50
    sem = asyncio.Semaphore(concurrent_limit)

    banner = BannerRequests()
    loop = asyncio.get_event_loop()

    start = time.time()
    counter = 0
    while True:
        try:
            data_set = loop.run_until_complete(banner.search(depts_terms, sem,
                                                         parse_all_courses))
            print(f"Downloaded and scraped {len(data_set)} departments data in"
                f" {time.time() - start:.2f} seconds")
            instructors = []
            sections = []
            meetings = []
            courses = []
    
            #print(data_set)
            return (instructors, sections, meetings, courses)
        except Exception as e:
            #print(str(e))
            counter = counter+1
            print("On Attempt: " + str(counter))
            continue
            
    #print(data_set)
    return (instructors, sections, meetings, courses)    

class Command(base.BaseCommand):
    """ Gets course information from banner and adds it to the database """

    def add_arguments(self, parser):
        parser.add_argument('--term', '-t', type=str,
                            help="A valid term code, such as 201931")
        parser.add_argument('--year', '-y', type=int,
                            help="A year to scrape all courses for, such as 2019")
        parser.add_argument('--recent', '-r', action='store_true',
                            help="Scrapes the most recent semester(s) for all locations")

    def handle(self, *args, **options):
        depts_terms = []
        start_all = time.time()
        term = None
        terms = None

        if options['term']:
            if options['year'] or options['recent']:
                print("ERROR: Too many arguments!")
                sys.exit(1)

            term = options['term']
            depts_terms = get_department_names([term])

        else:
            if options['year'] and options['recent']:
                print("ERROR: Too many arguments!")
                sys.exit(1)

            terms = get_all_terms()
            if options['year']:
                terms = get_all_terms(options['year'])
            elif options['recent']:
                terms = get_recent_terms()

            depts_terms = get_department_names(terms)

        instructors, sections, meetings, courses = get_course_data(depts_terms)
        #$%save_models(instructors, sections, meetings, courses, term, terms, options)

        print(f"Finished scraping in {time.time() - start_all:.2f} seconds")
