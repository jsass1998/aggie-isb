from django.core import management
from django.core.management import base

class Command(base.BaseCommand):

    def add_arguments(self, parser):
    
        parser.add_argument('--RMP', action='store_true')
        parser.add_argument('--CoursesRecent', action='store_true')

    def handle(self, *args, **options):
        if options['RMP']:
            management.call_command('UpdateProfessorRMPInfo')
        
        elif options['CoursesRecent']:
            management.call_command('scrape_depts_rev')
            management.call_command('scrape_courses_rev')
            management.call_command('UpdateProfessorRMPInfo')
            
        else:
            management.call_command('scrape_courses')
            management.call_command('scrape_grades')
            management.call_command('scrape_dept_rev')
            management.call_command('scrape_courses_rev')
            management.call_command('UpdateProfessorRMPInfo')
            
            