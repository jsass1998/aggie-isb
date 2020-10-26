from api.models import Course
from api.models import Professor
from api.models import Course_Prof
from api.models import Activity
from api.models import Section
from api.models import Schedule
from api.models import Activity_Instance
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
    office = "EABC 103",
    rate_my_prof = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1927583"
)
prof1.save()
prof2, created = Professor.objects.get_or_create(
    name = "John Michael Moore",
    dept = "Computer Science & Engineering",
    office = "HRBB 325",
    rate_my_prof = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2181152"
)
prof2.save()
prof3, created = Professor.objects.get_or_create(
    name = "Mohamad Riad Masri",
    dept = "Mathematics",
    office = "BLOC 641F",
    rate_my_prof = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1895628"
)
prof3.save()

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

activity1, created = Activity.objects.get_or_create(
    title = "CSCE 482-900",
    term = "FALL 2020"
)
activity1.save()
activity2, created = Activity.objects.get_or_create(
    title = "CSCE 436-500",
    term = "FALL 2020"
)
activity2.save()
activity3, created = Activity.objects.get_or_create(
    title = "MATH 407-500",
    term = "FALL 2020"
)
activity3.save()
activity4, created = Activity.objects.get_or_create(
    title = "Weekly Watch Party",
    term = "FALL 2020"
)
activity4.save()

section1, created = Section.objects.get_or_create(
    term = "FALL 2020",
    activity = activity1,
    course_prof = course_prof1,
    section_num = 900,
    honors = False
)
section1.save()
section2, created = Section.objects.get_or_create(
    term = "FALL 2020",
    activity = activity2,
    course_prof = course_prof2,
    section_num = 500,
    honors = False
)
section2.save()
section3, created = Section.objects.get_or_create(
    term = "FALL 2020",
    activity = activity3,
    course_prof = course_prof3,
    section_num = 500,
    honors = False
)
section3.save()

USER = User.objects.first()
schedule1, created = Schedule.objects.get_or_create(
    user = USER
)
schedule1.activities.set([activity1,activity2,activity3,activity4])
schedule1.save()

schedule2, created = Schedule.objects.get_or_create(
    user = USER
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