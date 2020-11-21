from django.db import models
import time

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)
    description = models.TextField(default="")

    def __str__(self):
        return self.course_id

    # def get_sections(self, term, campus):
    #     sections=[]
    #     for cp in self.course_prof_set.all():
    #         section_qset = cp.section_set.all().filter(
    #             term__exact = term,
    #             campus__exact = campus
    #         )
    #         for s in section_qset:
    #             sections = sections + [s.activity]
    #     return sections
    
    def get_sections(self, termcode):
        sections=[]
        for cp in self.course_prof_set.all():
            section_qset = cp.section_set.all().filter(
                term__exact = termcode
            )
            for s in section_qset:
                sections = sections + [s.activity]
        return sections

class Professor(models.Model):
    name = models.CharField(max_length=50)
    dept = models.CharField(max_length=50, default="")
    office = models.CharField(max_length=20, default="")
    rating_class = models.CharField(max_length=20, default="average")
    overall_rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    num_ratings = models.IntegerField(null=True)
    rmp_link = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)+': '+self.name

class Course_Prof(models.Model):
    #Course-Prof table for storing grade-dist info
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    professor = models.ForeignKey(
        Professor,
        on_delete=models.CASCADE
    )
    percent_A = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percent_B = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percent_C = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percent_D = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percent_F = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    percent_Q = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ('course', 'professor')

    def __str__(self):
        return "("+str(self.course)+", "+str(self.professor)+")"

class Activity(models.Model):
    title = models.CharField(max_length=100)
    term = models.CharField(max_length=16)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null = True
    )

    def __str__(self):
        return self.title+" - "+self.term

    def conflicts_with(self, other_activity):
        for a in self.activity_instance_set.all():
            for b in other_activity.activity_instance_set.all():
                if a.conflicts_with(b):
                    return True
        return False

    def get_instances_list(self):
        instances_queryset = self.activity_instance_set.all()
        instances_list = [instance for instance in instances_queryset]
        return instances_list

class Section(models.Model):
    #each Section is a special type of Activity
    activity = models.OneToOneField(
        Activity,
        on_delete=models.CASCADE,
        primary_key=True
    )

    #many Sections can exist for every Course_Prof pair
    course_prof = models.ForeignKey(
        Course_Prof,
        on_delete=models.CASCADE
    )

    term = models.CharField(max_length=32)
    section_num = models.IntegerField()
    crn = models.IntegerField()
    credit_hours = models.IntegerField()
    campus = models.CharField(max_length=64, default="College Station")
    honors = models.BooleanField(default=False)
    web = models.BooleanField(default=False)
    total_seats = models.IntegerField(default=0)
    seats_taken = models.IntegerField(default=0)

    # of students who have this section in a schedule
    interested_students = models.IntegerField(default=0)

    class Meta:
        unique_together = ('course_prof', 'term', 'section_num')

    def __str__(self):
        return "Section: "+self.activity.title+", "+self.term

    def update_interested_students(self):
       self.interested_students = self.activity.schedule_set.all().order_by(
           'user'
       ).distinct(
           'user'
       ).count()

class Activity_Instance(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE
    )
    location = models.CharField(max_length=64)
    day = models.CharField(max_length=8)
    starttime = models.TimeField()
    endtime = models.TimeField()

    def __str__(self):
        s="("
        s=s+self.activity.title+", "
        s=s+self.activity.term+", "
        s=s+self.day+", "
        s=s+str(self.starttime)+"-"+str(self.endtime)
        s=s+")"
        return s

    def conflicts_with(self, other_instance):
        b = self.day == other_instance.day
        b = b and self.starttime < other_instance.endtime
        b = b and self.endtime > other_instance.starttime
        return b

class Schedule(models.Model):
    #Many Schedules can be associated with a User
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True
    )
    #A schedule can have many Activities
    #An Activity can be part of many Schedules
    activities = models.ManyToManyField(Activity)
    term = models.CharField(max_length=16)
    campus = models.CharField(max_length=16, default="College Station")
    user_saved = models.BooleanField(default=False)
    avg_starttime = models.TimeField(default="12:00:00")
    avg_endtime = models.TimeField(default="15:00:00")
    avg_day_length = models.TimeField(default="05:00:00")
    free_on_monday = models.BooleanField(default=False)
    free_on_tuesday = models.BooleanField(default=False)
    free_on_wednesday = models.BooleanField(default=False)
    free_on_thursday = models.BooleanField(default=False)
    free_on_friday = models.BooleanField(default=False)
    num_free_days = models.IntegerField(default=0)

    def __str__(self):
        s=str(self.id)+": "+str(self.user)
        s=s+" ("+str(self.activities.count())+" activities)"
        return s

    def conflicts_with(self, activity):
        for a in self.activities.all():
            if a.conflicts_with(activity):
                return True
        return False

    def get_activities_list(self):
        activities_queryset = self.activities.all()
        activities_list = [activity for activity in activities_queryset]
        return activities_list

    def add_activity(self, activity):
        curr_activities = self.get_activities_list()
        new_activities = curr_activities+[activity]
        self.activities.set(new_activities)

    def get_instances(self):
        instance_list = []
        for activity in self.activities.all():
            instance_list = instance_list + activity.get_instances_list()
        instance_ids = [instance.id for instance in instance_list]
        instances = Activity_Instance.objects.all().filter(
            id__in=instance_ids
        )
        return instances

    def compute_avg_starttime(self):
        schedule_instances = self.get_instances()
        week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        stime_sum = 0
        for day in week:
            daily_instances = schedule_instances.filter(
                day__exact = day,
            )
            if daily_instances.count() is not 0:
                stime=daily_instances.order_by(
                    'starttime'
                ).first().starttime
                stime_sec = stime.hour*3600+stime.minute*60
                stime_sum = stime_sum + stime_sec
        stime_avg_sec=0
        if self.num_free_days is not 5:
            stime_avg_sec = round(stime_sum / (5-self.num_free_days))
        stime_avg = time.strftime('%H:%M:%S', time.gmtime(stime_avg_sec))
        self.__setattr__("avg_starttime", stime_avg)
        return stime_avg
            
    def compute_avg_endtime(self):
        schedule_instances = self.get_instances()
        week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        etime_sum = 0
        for day in week:
            daily_instances = schedule_instances.filter(
                day__exact = day,
            )
            if daily_instances.count() is not 0:
                etime = daily_instances.order_by(
                    '-endtime'
                ).first().endtime
                etime_sec = etime.hour*3600+etime.minute*60
                etime_sum = etime_sum + etime_sec
        etime_avg_sec = 0
        if self.num_free_days is not 5:
            etime_avg_sec = round(etime_sum / (5-self.num_free_days))
        etime_avg = time.strftime('%H:%M:%S', time.gmtime(etime_avg_sec))
        self.__setattr__("avg_endtime", etime_avg)
        return etime_avg

    def compute_avg_day_length(self):
        schedule_instances = self.get_instances()
        week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        day_length_sum = 0
        for day in week:
            daily_instances = schedule_instances.filter(
                day__exact = day,
            )
            if daily_instances.count() is not 0:
                stime = daily_instances.order_by(
                    'starttime'
                ).first().starttime
                etime = daily_instances.order_by(
                    '-endtime'
                ).first().endtime
                stime_sec = stime.hour*3600+stime.minute*60
                etime_sec = etime.hour*3600+etime.minute*60
                day_length_sec = etime_sec-stime_sec
                day_length_sum = day_length_sum+day_length_sec
        day_length_avg_sec = 0
        if self.num_free_days is not 5:
            day_length_avg_sec = round(day_length_sum / (5-self.num_free_days))
        day_length_avg = time.strftime('%H:%M:%S', time.gmtime(day_length_avg_sec))
        self.__setattr__("avg_day_length", day_length_avg)
        return day_length_avg

    def find_free_days(self):
        schedule_instances = self.get_instances()
        week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        free_on = {
            "monday": "free_on_monday",
            "tuesday": "free_on_tuesday",
            "wednesday": "free_on_wednesday",
            "thursday": "free_on_thursday",
            "friday": "free_on_friday"
        }
        free_day_count = 0
        for day in week:
            daily_instances = schedule_instances.filter(
                day__exact = day,
            )
            if daily_instances.count() is 0:
                self.__setattr__(free_on[day], True)
                free_day_count = free_day_count+1
        self.__setattr__("num_free_days", free_day_count)
        return free_day_count

    def generate_descriptors(self):
        self.find_free_days()
        self.compute_avg_starttime()
        self.compute_avg_endtime()
        self.compute_avg_day_length()

class Term_Location(models.Model):
    term = models.CharField(max_length=16)
    location = models.CharField(max_length=32)

    def __str__(self):
        return self.term + " - " + self.location