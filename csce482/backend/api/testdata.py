from api.models import Course
from api.models import Professor
from api.models import Course_Prof
from api.models import Activity
from api.models import Section
from api.models import Schedule
from api.models import Activity_Instance
from users.models import User

course1 = Course.objects.create(
    course_id = "CSCE 482",
    title = "Senior Capstone Design"
)
course1.save()
course2 = Course.objects.create(
    course_id = "CSCE 436",
    title = "Human-Computer Interaction"
)
course2.save()
course3 = Course.objects.create(
    course_id = "MATH 407",
    title = "Complex Variables"
)
course3.save()

prof1 = Professor.objects.create(
    name = "Tracy Hammond",
    dept = "Computer Science & Engineering",
    office = "EABC 103",
    rate_my_prof = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1927583"
)
prof1.save()
prof2 = Professor.objects.create(
    name = "John Michael Moore",
    dept = "Computer Science & Engineering",
    office = "HRBB 325",
    rate_my_prof = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=2181152"
)
prof2.save()
prof3 = Professor.objects.create(
    name = "Mohamad Riad Masri",
    dept = "Mathematics",
    office = "BLOC 641F",
    rate_my_prof = "https://www.ratemyprofessors.com/ShowRatings.jsp?tid=1895628"
)
prof3.save()

course_prof1 = Course_Prof.objects.create(
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
course_prof2 = Course_Prof.objects.create(
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
course_prof3 = Course_Prof.objects.create(
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

activity1 = Activity.objects.create(
    title = "CSCE 482-900",
    term = "FALL 2020"
)
activity1.save()
activity2 = Activity.objects.create(
    title = "CSCE 436-500",
    term = "FALL 2020"
)
activity2.save()
activity3 = Activity.objects.create(
    title = "MATH 407-500",
    term = "FALL 2020"
)
activity3.save()
activity4 = Activity.objects.create(
    title = "Weekly Watch Party",
    term = "FALL 2020"
)
activity4.save()

USER = User.objects.first()
schedule1 = Schedule.objects.create(
    user = USER
)
schedule1.activities.set([activity1,activity2,activity3,activity4])
schedule1.save()

schedule2 = Schedule.objects.create(
    user = USER
)
schedule2.activities.set([activity1,activity2,activity3])
schedule2.save()

act_inst1 = Activity_Instance.objects.create(
    activity = activity1,
    location = "ONLINE",
    day = "MON",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst1.save()
act_inst2 = Activity_Instance.objects.create(
    activity = activity1,
    location = "ONLINE",
    day = "MON",
    starttime = "09:30:00",
    endtime = "12:00:00"
)
act_inst2.save()
act_inst3 = Activity_Instance.objects.create(
    activity = activity1,
    location = "ONLINE",
    day = "WED",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst3.save()
act_inst4 = Activity_Instance.objects.create(
    activity = activity1,
    location = "ONLINE",
    day = "WED",
    starttime = "09:00:00",
    endtime = "09:25:00"
)
act_inst4.save()
act_inst5 = Activity_Instance.objects.create(
    activity = activity2,
    location = "ONLINE",
    day = "MON",
    starttime = "14:55:00",
    endtime = "15:45:00"
)
act_inst5.save()
act_inst6 = Activity_Instance.objects.create(
    activity = activity2,
    location = "ONLINE",
    day = "WED",
    starttime = "14:55:00",
    endtime = "15:45:00"
)
act_inst6.save()
act_inst7 = Activity_Instance.objects.create(
    activity = activity2,
    location = "ONLINE",
    day = "FRI",
    starttime = "14:55:00",
    endtime = "15:45:00"
)
act_inst7.save()
act_inst8 = Activity_Instance.objects.create(
    activity = activity3,
    location = "BLOC 166",
    day = "TUE",
    starttime = "17:00:00",
    endtime = "18:15:00"
)
act_inst8.save()
act_inst9 = Activity_Instance.objects.create(
    activity = activity3,
    location = "BLOC 166",
    day = "THU",
    starttime = "17:00:00",
    endtime = "18:15:00"
)
act_inst9.save()
act_inst10 = Activity_Instance.objects.create(
    activity = activity4,
    location = "ONLINE",
    day = "WED",
    starttime = "18:00:00",
    endtime = "21:00:00"
)
act_inst10.save()