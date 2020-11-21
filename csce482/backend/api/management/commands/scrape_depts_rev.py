# Called to execute the beginning of scaping courses
import time
import datetime
from typing import List, Tuple
import os

from django.core.management import base
from api.banner_requests import BannerRequests
#from scraper.models import Department
from api.management.commands.utils.scraper_utils import get_all_terms

def parse_departments(json, term) -> List[Tuple[str,str,str,str]]:
    """ Takes in a json list of departments and returns a list of Department objects """
    
    departments = []

    for dept in json:
        departments.append((f"{dept['code']}{term}", dept["code"], dept["description"], term))

    return departments

def scrape_departments(term) -> List[Tuple[str,str,str,str]]:
    """ Takes term input and collects json object of departments """

    request = BannerRequests()
    json = request.get_departments(term)

    return parse_departments(json, term)

class Command(base.BaseCommand):
    """ Gets all departments from banner and adds them to the database """

    def add_arguments(self, parser):
        parser.add_argument('--term', '-t', type=str,
                            help="A valid term code, such as 201931.")

    def handle(self, *args, **options):
        start = time.time()
        depts = []

        if options['term']:
            depts = scrape_departments(options['term'])
        else:
            terms = get_all_terms()

            for term in terms:
                print(f"Scraping depts for {term}")
                depts.extend(scrape_departments(term))
        
        try:
            os.remove("departments.txt")
        except Exception as e:
            print(str(e))
        
        f = open("departments.txt", "w")
        f.close()
        
        for dept in depts:
            f = open("departments.txt", "a")
            dept_zero = ''.join(c for c in dept[0] if c.isdigit())
            if dept_zero[5] == '1': #this line is filtering to just college station departments.
                f.write(dept_zero + " " + dept[1] + " " + dept[2] + " " + dept[3] + " F" + "\r\n")
            f.close()

        end = time.time()
        seconds_elapsed = int(end - start)
        time_delta = datetime.timedelta(seconds=seconds_elapsed)
        print(f"Finished scraping {len(depts)} departments in {time_delta}")
