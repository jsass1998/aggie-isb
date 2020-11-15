from .models import Course
from .models import Professor
from .models import Course_Prof
from .models import Activity
from .models import Section
from .models import Schedule
from .models import Activity_Instance
from users.models import User

def generate_schedules(schedule_user, schedule_term, schedule_campus, selected_courses, blocked_times):
    count = len(selected_courses)+1
    section_lists = [course.get_sections(schedule_term, schedule_campus) for course in selected_courses]
    
    blocked_time_activity = Activity.objects.create(
        title = 'Blocked Time',
        term = schedule_term
    )
    if schedule_user is not None:
        blocked_time_activity.user = schedule_user
    blocked_time_activity.save()
    for (day, starttime, endtime) in blocked_times:
        blocked_time_instance = Activity_Instance.objects.get_or_create(
            activity = blocked_time_activity,
            location = "variable",
            day = day,
            starttime = starttime,
            endtime = endtime
        )[0]
        blocked_time_instance.save()
    activity_lists = section_lists + [[blocked_time_activity]]
    
    schedules = refine_schedules(schedule_user, schedule_term, schedule_campus, activity_lists, count-1)
    return schedules

def refine_schedules(schedule_user, schedule_term, schedule_campus, activity_lists, count):
    if count == 0:
        schedules = []
        for activity in activity_lists[0]:
            new_schedule = Schedule.objects.create(
                term = schedule_term,
                campus = schedule_campus
            )
            if schedule_user is not None:
                new_schedule.user = schedule_user
            
            new_schedule.activities.set([activity])
            if schedule_user is not None:
                new_schedule.save()

            schedules.append(new_schedule)
        return schedules
    else:
        schedules = refine_schedules(schedule_user, schedule_term, schedule_campus, activity_lists, count-1)
        next_schedules = []
        for schedule in schedules:
            if count == len(activity_lists)-1:
                schedule.generate_descriptors()
            for activity in activity_lists[count]:
                if not schedule.conflicts_with(activity):
                    curr_activities = schedule.get_activities_list()
                    next_schedule = Schedule.objects.create(
                        term = schedule_term,
                        campus = schedule_campus
                    )
                    if schedule_user is not None:
                        next_schedule.user = schedule_user
                    
                    next_schedule.activities.set(curr_activities + [activity])
                    if schedule_user is not None:
                        next_schedule.save()

                    next_schedules.append(next_schedule)
            schedule.delete()
        return next_schedules

