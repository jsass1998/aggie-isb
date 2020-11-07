import asyncio
import concurrent
import datetime
import time
from typing import List

from django.core.management import base
from django.db import transaction

from scraper import models as scraper_models
from scraper.management.commands import section_parser as parser
from scraper.management.commands import shared_functions


async def scrape_departments(term_code: int, depts: List[str]):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, shared_functions.sections, term_code, dept)
            for dept in depts
        ]
        parameters = []
        for soup in await asyncio.gather(*futures):
            if not soup:
                continue
            results = parser.parse_sections(soup)
            parameters += results
        return parameters


def is_current_term(term_code: str) -> bool:
    this_year = datetime.date.today().year
    return int(term_code[:4]) >= this_year


class Command(base.BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--shallow",
            action="store_true",
            help="Scrape terms from this and next year",
        )

    def handle(self, *args, **options):
        full_start = time.time()
        term_codes = shared_functions.term_codes()
        if options["shallow"]:
            term_codes = filter(is_current_term, term_codes)
        for term_code in term_codes:
            print("----------------------")
            print(term_code)
            print("----------------------")
            loop = asyncio.get_event_loop()
            depts = shared_functions.depts(term_code)
            start = time.time()
            parameters = loop.run_until_complete(scrape_departments(term_code, depts))
            end = time.time()
            td = datetime.timedelta(seconds=int(end - start))
            print(f"{len(parameters)} sections collected in {td}. Beginning indexing.")

            with transaction.atomic():
                courses = {}
                for section_fields, meeting_fields in parameters:
                    section_id = f"{section_fields['crn']}_{term_code}"
                    course_id = (
                        f"{section_fields['dept']}-{section_fields['course_num']}"
                    )
                    if not course_id in courses:
                        course = scraper_models.Course.objects.filter(
                            id=course_id
                        ).first()
                        if course:
                            courses[course_id] = course
                        else:
                            course = scraper_models.Course(
                                id=course_id,
                                dept=section_fields["dept"],
                                course_num=section_fields["course_num"],
                                min_credits=section_fields["min_credits"],
                                max_credits=section_fields["max_credits"],
                                name=section_fields["name"].title(),
                            )
                            course.save()
                            courses[course_id] = course
                    section = scraper_models.Section(
                        id=section_id, term_code=int(term_code), **section_fields
                    )
                    section.save()
                    if meeting_fields:
                        for i, m in enumerate(meeting_fields):
                            meeting_id = section_id + "_" + str(i + 1)
                            meeting = scraper_models.Meeting(id=meeting_id, **m)
                            meeting.save()
                            section.meetings.add(meeting)
        td = datetime.timedelta(seconds=int(time.time() - full_start))
        print(f"Finished scraping all sections in {td}.")
