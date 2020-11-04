from .models import Course
from .models import Professor
from .models import Course_Prof
from .models import Activity
from .models import Section
from .models import Schedule
from .models import Activity_Instance
from users.models import User

def generate_schedules(schedule_user, selected_courses, schedule_term):
    count = len(selected_courses)
    section_lists = [course.get_sections(schedule_term) for course in selected_courses]
    schedules = refine_schedules(schedule_user, schedule_term, section_lists, count-1)
    return schedules

def refine_schedules(schedule_user, schedule_term, section_lists, count):
    if count == 0:
        schedules = []
        for section in section_lists[0]:
            new_schedule = Schedule.objects.create(
                user = schedule_user,
                term = schedule_term
            )
            new_schedule.activities.set([section])
            new_schedule.save()
            schedules.append(new_schedule)
        return schedules
    else:
        schedules = refine_schedules(schedule_user, schedule_term, section_lists, count-1)
        next_schedules = []
        for schedule in schedules:
            for section in section_lists[count]:
                if not schedule.conflicts_with(section):
                    curr_sections = schedule.get_sections()
                    next_schedule = Schedule.objects.create(
                        user = schedule_user,
                        term = schedule_term
                    )
                    next_schedule.activities.set(curr_sections + [section])
                    next_schedule.save()
                    next_schedules.append(next_schedule)
        return next_schedules