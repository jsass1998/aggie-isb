from django.core import management
from django.core.management import base

class Command(base.BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--RMP', '-r', type=str,
                            help="just updating RateMyProfessor info")
        parser.add_argument('--CoursesRecent', '-c', type=int,
                            help="A year to scrape all courses for, such as 2019")

    def handle(self, *args, **options):
        if options['RMP']:
            management.call_command('UpdateProfessorRMPInfo')
        
        elif options['CoursesRecent']:
            management.call_command('scrape_dept_rev')
            management.call_command('scrape_courses_rev')
            management.call_command('UpdateProfessorRMPInfo')
            
        else:
            management.call_command('scrape_courses')
            management.call_command('scrape_grades')
            management.call_command('scrape_dept_rev')
            management.call_command('scrape_courses_rev')
            management.call_command('UpdateProfessorRMPInfo')
            
            