from django.core.management import base
from api import models as scraper_models
from api.management.commands import shared_functions, pdf_parser

import requests
from typing import List
import bs4
import os


ROOT_URL = "http://web-as.tamu.edu/gradereport/"
PDF_URL = "http://web-as.tamu.edu/gradereport/PDFReports/{}/grd{}{}.pdf"
PDF_DOWNLOAD_DIR = os.path.abspath("documents/pdfs")

SPRING, SUMMER, FALL = "1", "2", "3"


def years() -> List[int]:
    r = requests.get(ROOT_URL)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, "lxml")
    options = soup.select("#ctl00_plcMain_lstGradYear > option")
    return [int(o["value"]) for o in options]


def colleges() -> List[str]:
    r = requests.get(ROOT_URL)
    r.raise_for_status()

    soup = bs4.BeautifulSoup(r.text, "lxml")
    options = soup.select("#ctl00_plcMain_lstGradCollege > option")
    return [o["value"] for o in options]


def download_pdf(year_semester: str, college: str) -> str:
    """Downloads a PDF from the given URL.

    Args:
        year_semester: A 4-digit year, followed by an integer indicating            semester
        college: The abbreviation for the college, as found on the registrar
    Returns:
        The path to the downloaded PDF file.
    """
    url = PDF_URL.format(year_semester, year_semester, college)
    filename = url.split("/")[-1]
    path = os.path.join(PDF_DOWNLOAD_DIR, filename)

    r = requests.get(url)
    try:
        r.raise_for_status()
        if os.path.isfile(path):
            return path
        with open(path, "wb+") as f:
            f.write(r.content)
            return path
    except requests.exceptions.HTTPError as e:
        if e.response.status_code != 404:
            raise e


def build_term_code(year_semester: str, abbr: str) -> str:
    """Creates a term_code from a year + semester string and an abbreviation.
    Args:
        year_semester: A string in the format "YYYYS" where Y=year and S is in {1, 2, 3}
        abbr: A short code indicating what college is being parsed.
    Returns:
        A 6-char string whose digits are: YYYYSU where U is in {1, 2, 3}
    """
    if abbr != "GV" and abbr != "QT":
        return year_semester + "1"
    else:
        if abbr == "GV":
            return year_semester + "2"
        else:
            return year_semester + "3"


class Command(base.BaseCommand):
    def handle(self, *args, **kwargs):
        #courses_missed = []
        yrs = years()
        college_abbrevs = colleges()
        for year in yrs:
            for semester in [SPRING, SUMMER, FALL]:
                year_semester = str(year) + semester
                print(year_semester)
                for college in college_abbrevs:
                    print(college)
                    term = build_term_code(year_semester, college)
                    pdf_path = download_pdf(year_semester, college)
                    if pdf_path:
                        distribution_fields = pdf_parser.parse_pdf(pdf_path)

                        iterator = 0
                        for dist in distribution_fields:
                            iterator += 1
                            #*print(iterator)
                        
                            #***I need to generate a course object, fetch/generate a professor object
                            #***I need to get these two objects and associate them via course_prof object
                            
                            ##grades, (dept, course_num, section_num), gpa = dist
                            ##section = scraper_models.Section.objects.filter(
                            ##    dept=dept,
                            ##    course_num=course_num,
                            ##    section_num=section_num,
                            ##    term=int(term),
                            ##).first()
                            
                            ##if section:
                            ##    grades, _ = scraper_models.Grades.objects.update_or_create(
                            ##        section=section, defaults={**grades, "gpa": gpa}
                            ##    )
                            ##    section.grades = grades
                            
                            grades, (dept, course_num, section_num, prof_data), gpa = dist
                            
                            try:
                                ###course object
                                _course_id = str(dept) + "-" + str(course_num)
                                #print("Starting try: " + _course_id)
                                valid_course = scraper_models.Course.objects.get(course_id = _course_id)
                            except Exception as e:
                                #courses_missed.append(str(_course_id) + "-" + year_semester)
                                print(str(e))
                                new_course = scraper_models.Course.objects.get_or_create(
                                    course_id = _id,
                                    title = "Outdated Course: No Info"
                                )[0]
                                continue                            
                             
                            try: 
                                ###course prof object
                                new_prof = scraper_models.Professor.objects.get_or_create(
                                    name = prof_data,
                                    dept = dept,
                                    office = ""
                                )[0]
                                new_prof.save()
                            except Exception as e:
                                print(str(e))
                                continue                                
                                
                            try:     
                                ###new course prof objec
                                new_course_prof = scraper_models.Course_Prof.objects.get_or_create(
                                   course = valid_course,
                                   professor = new_prof 
                                )[0]
                                new_course_prof.save()
                            except Exception as e:
                                print(str(e))
                                continue     
                                
                            try:    
                                new_activity = scraper_models.Activity.objects.get_or_create(
                                    title = _course_id + "-" + str(section_num),
                                    term = year_semester
                                )[0]
                                new_activity.save()
                            except Exception as e:
                                print(str(e))
                                continue 
                                
                            try:    
                                ###section object
                                new_section = scraper_models.Section.objects.get_or_create(
                                    activity = new_activity,
                                    course_prof = new_course_prof,
                                    term = year_semester,
                                    section_num = section_num,
                                    crn = 0,
                                    credit_hours = 0,
                                    total_seats = 0
                                )[0]
                                new_section.save()
                            except Exception as e:
                                print(str(e))
                                continue     
                                
        #print(*courses_missed)

