from django.core import management
from django.core.management import base

class Command(base.BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--OneCommand')    
        parser.add_argument('--CoursesRecent', action='store_true')

    def handle(self, *args, **options):
        if options['CoursesRecent']:
            management.call_command('scrape_depts_rev')
            management.call_command('scrape_courses_rev')
            management.call_command('UpdateProfessorRMPInfo')
            
        elif options['OneCommand']:
            command = options['OneCommand']
            management.call_command(command)
            
        else:
            management.call_command('scrape_courses')
            management.call_command('scrape_grades')
            management.call_command('scrape_dept_rev')
            management.call_command('scrape_courses_rev')
            management.call_command('UpdateProfessorRMPInfo')