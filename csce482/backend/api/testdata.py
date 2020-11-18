from api.models import Course
from api.models import Professor
from api.models import Course_Prof
from api.models import Activity
from api.models import Section
from api.models import Schedule
from api.models import Activity_Instance
from api.models import Term_Location
from users.models import User

course1, created = Course.objects.get_or_create(
    course_id = "CSCE 482",
    title = "Senior Capstone Design"
)
course1.save()
course2, created = Course.objects.get_or_create(
    course_id = "CSCE 436",
    title = "Human-Computer Interaction"
)
course2.save()
course3, created = Course.objects.get_or_create(
    course_id = "MATH 407",
    title = "Complex Variables"
)
course3.save()

prof1, created = Professor.objects.get_or_create(
    name = "Tracy Hammond",
    dept = "Computer Science & Engineering",
    office = "EABC 103"
)
prof1.save()
prof2, created = Professor.objects.get_or_create(
    name = "John Michael Moore",
    dept = "Computer Science & Engineering",
    office = "HRBB 325"
)
prof2.save()
prof3, created = Professor.objects.get_or_create(
    name = "Mohamad Riad Masri",
    dept = "Mathematics",
    office = "BLOC 641F"
)
prof3.save()
prof4, created = Professor.objects.get_or_create(
    name = "Rabinarayan Mahapatra",
    dept = "Computer Science & Engineering",
    office = "HRBB 520B"
)
prof4.save()
prof5, created = Professor.objects.get_or_create(
    name = "Aaron Michael Kingery",
    dept = "Computer Science & Engineering",
    office = "ONLINE"
)
prof5.save()


course_prof1, created = Course_Prof.objects.get_or_create(
    course = course1,
    professor = prof1,
    percent_A = 89.94,
    percent_B = 8.18,
    percent_C = 1.89,
    percent_D = 0,
    percent_F = 0,
    percent_Q = 0
)
course_prof1.save()
course_prof2, created = Course_Prof.objects.get_or_create(
    course = course2,
    professor = prof2,
    percent_A = 58.89,
    percent_B = 35.19,
    percent_C = 4.07,
    percent_D = 0.74,
    percent_F = 0,
    percent_Q = 1.11
)
course_prof2.save()
course_prof3, created = Course_Prof.objects.get_or_create(
    course = course3,
    professor = prof3,
    percent_A = 27.78,
    percent_B = 16.67,
    percent_C = 22.22,
    percent_D = 16.67,
    percent_F = 0,
    percent_Q = 16.67
)
course_prof3.save()
course_prof4, created = Course_Prof.objects.get_or_create(
    course = course1,
    professor = prof4,
    percent_A = 0,
    percent_B = 0,
    percent_C = 0,
    percent_D = 0,
    percent_F = 0,
    percent_Q = 0
)
course_prof4.save()
course_prof5, created = Course_Prof.objects.get_or_create(
    course = course1,
    professor = prof5,
    percent_A = 0,
    percent_B = 0,
    percent_C = 0,
    percent_D = 0,
    percent_F = 0,
    percent_Q = 0
)
course_prof5.save()

activity1, created = Activity.objects.get_or_create(
    title = "CSCE 482-900",
    term = "202031"
)
activity1.save()
activity2, created = Activity.objects.get_or_create(
    title = "CSCE 436-500",
    term = "202031"
)
activity2.save()
activity3, created = Activity.objects.get_or_create(
    title = "MATH 407-500",
    term = "202031"
)
activity3.save()
activity4, created = Activity.objects.get_or_create(
    title = "Weekly Watch Party",
    term = "202031"
)
activity4.save()
activity5, created = Activity.objects.get_or_create(
    title = "CSCE 482-901",
    term = "202031"
)
activity5.save()
activity6, created = Activity.objects.get_or_create(
    title = "CSCE 482-930",
    term = "202031"
)
activity6.save()

section1, created = Section.objects.get_or_create(
    term = "202031",
    campus = "College Station",
    activity = activity1,
    course_prof = course_prof1,
    section_num = 900,
    honors = False,
    crn = 35464,
    credit_hours = 3
)
section1.save()
section2, created = Section.objects.get_or_create(
    term = "202031",
    campus = "College Station",
    activity = activity2,
    course_prof = course_prof2,
    section_num = 500,
    honors = False,
    crn = 37727,
    credit_hours = 3
)
section2.save()
section3, created = Section.objects.get_or_create(
    term = "202031",
    campus = "College Station",
    activity = activity3,
    course_prof = course_prof3,
    section_num = 500,
    honors = False,
    crn = 11997,
    credit_hours = 3
)
section3.save()
section4, created = Section.objects.get_or_create(
    term = "202031",
    campus = "College Station",
    activity = activity5,
    course_prof = course_prof4,
    section_num = 901,
    honors = False,
    crn = 35465,
    credit_hours = 3
)
section4.save()
section5, created = Section.objects.get_or_create(
    term = "202031",
    campus = "College Station",
    activity = activity6,
    course_prof = course_prof5,
    section_num = 930,
    honors = False,
    crn = 39786,
    credit_hours = 3
)
section5.save()

USER = User.objects.first()
schedule1, created = Schedule.objects.get_or_create(
    user = USER,
    term = "202031"
)
schedule1.activities.set([activity1,activity2,activity3,activity4])
schedule1.save()

schedule2, created = Schedule.objects.get_or_create(
    user = USER,
    term = "202031"
)
schedule2.activities.set([activity1,activity2,activity3])
schedule2.save()

act_inst1, created = Activity_Instance.objects.get_or_create(
    activity = activity1,
    location = "ONLINE",
    day = "MON",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst1.save()
act_inst2, created = Activity_Instance.objects.get_or_create(
    activity = activity1,
    location = "ONLINE",
    day = "MON",
    starttime = "09:30:00",
    endtime = "12:00:00"
)
act_inst2.save()
act_inst3, created = Activity_Instance.objects.get_or_create(
    activity = activity1,
    location = "ONLINE",
    day = "WED",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst3.save()
act_inst4, created = Activity_Instance.objects.get_or_create(
    activity = activity1,
    location = "ONLINE",
    day = "WED",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst4.save()
act_inst5, created = Activity_Instance.objects.get_or_create(
    activity = activity2,
    location = "ONLINE",
    day = "MON",
    starttime = "14:55:00",
    endtime = "15:45:00"
)
act_inst5.save()
act_inst6, created = Activity_Instance.objects.get_or_create(
    activity = activity2,
    location = "ONLINE",
    day = "WED",
    starttime = "14:55:00",
    endtime = "15:45:00"
)
act_inst6.save()
act_inst7, created = Activity_Instance.objects.get_or_create(
    activity = activity2,
    location = "ONLINE",
    day = "FRI",
    starttime = "14:55:00",
    endtime = "15:45:00"
)
act_inst7.save()
act_inst8, created = Activity_Instance.objects.get_or_create(
    activity = activity3,
    location = "BLOC 166",
    day = "TUE",
    starttime = "17:00:00",
    endtime = "18:15:00"
)
act_inst8.save()
act_inst9, created = Activity_Instance.objects.get_or_create(
    activity = activity3,
    location = "BLOC 166",
    day = "THU",
    starttime = "17:00:00",
    endtime = "18:15:00"
)
act_inst9.save()
act_inst10, created = Activity_Instance.objects.get_or_create(
    activity = activity4,
    location = "ONLINE",
    day = "WED",
    starttime = "18:00:00",
    endtime = "21:00:00"
)
act_inst10.save()
act_inst11, created = Activity_Instance.objects.get_or_create(
    activity = activity5,
    location = "EABA 118",
    day = "TUE",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst11.save()
act_inst12, created = Activity_Instance.objects.get_or_create(
    activity = activity5,
    location = "EABA 118",
    day = "TUE",
    starttime = "09:30:00",
    endtime = "12:00:00"
)
act_inst12.save()
act_inst13, created = Activity_Instance.objects.get_or_create(
    activity = activity5,
    location = "EABA 118",
    day = "THU",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst13.save()
act_inst14, created = Activity_Instance.objects.get_or_create(
    activity = activity5,
    location = "EABA 118",
    day = "THU",
    starttime = "09:30:00",
    endtime = "12:00:00"
)
act_inst14.save()
act_inst15, created = Activity_Instance.objects.get_or_create(
    activity = activity6,
    location = "EABA 118",
    day = "TUE",
    starttime = "14:00:00",
    endtime = "14:25:00"
)
act_inst15.save()
act_inst16, created = Activity_Instance.objects.get_or_create(
    activity = activity6,
    location = "EABA 118",
    day = "TUE",
    starttime = "14:30:00",
    endtime = "17:00:00"
)
act_inst16.save()
act_inst17, created = Activity_Instance.objects.get_or_create(
    activity = activity6,
    location = "EABA 118",
    day = "THU",
    starttime = "14:00:00",
    endtime = "14:25:00"
)
act_inst17.save()
act_inst18, created = Activity_Instance.objects.get_or_create(
    activity = activity6,
    location = "EABA 118",
    day = "THU",
    starttime = "14:30:00",
    endtime = "17:00:00"
)
act_inst18.save()

term_loc1, created = Term_Location.objects.get_or_create(
    term = "FALL 2020",
    location = "College Station"
)
term_loc2, created = Term_Location.objects.get_or_create(
    term = "SPRING 2021",
    location = "College Station"
)
term_loc3, created = Term_Location.objects.get_or_create(
    term = "SUMMER 2021",
    location = "College Station"
)
term_loc4, created = Term_Location.objects.get_or_create(
    term = "FALL 2020",
    location = "Galveston"
)
term_loc5, created = Term_Location.objects.get_or_create(
    term = "SPRING 2021",
    location = "Galveston"
)
term_loc6, created = Term_Location.objects.get_or_create(
    term = "SUMMER 2021",
    location = "Qatar"
)