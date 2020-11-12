from django.core import management
from django.core.management import base
import time

class Command(base.BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--OneCommand')    
        parser.add_argument('--CoursesRecent', action='store_true')

    def handle(self, *args, **options):
        if options['CoursesRecent']:
            management.call_command('scrape_depts_rev')
            time.sleep(60)
            management.call_command('scrape_courses_rev')
            time.sleep(60)
            management.call_command('UpdateProfessorRMPInfo')
            
        elif options['OneCommand']:
            command = options['OneCommand']
            management.call_command(command)
            
        else:
            start = time.time()
            management.call_command('scrape_courses')
            time.sleep(60)
            management.call_command('scrape_grades')
            time.sleep(60)
            management.call_command('scrape_depts_rev')
            time.sleep(60)
            management.call_command('scrape_courses_rev')
            time.sleep(60)
            management.call_command('UpdateProfessorRMPInfo')
            end = time.time()
            
            seconds_elapsed = int(end - start)
            time_delta = datetime.timedelta(seconds=seconds_elapsed)
            print(f"Finished scraping in {time_delta/60} minutes")