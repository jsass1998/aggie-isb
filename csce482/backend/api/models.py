from django.db import models

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.course_id

    def get_sections(self, t):
        sections=[]
        for cp in self.course_prof_set.all():
            for s in cp.section_set.all().filter(term__exact = t):
                sections = sections + [s.activity]
        return sections

class Professor(models.Model):
    name = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    office = models.CharField(max_length=20)
    rating_class = models.CharField(max_length=20)
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
    campus = models.CharField(max_length=64)
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
        on_delete=models.CASCADE
    )
    #A schedule can have many Activities
    #An Activity can be part of many Schedules
    activities = models.ManyToManyField(Activity)
    term = models.CharField(max_length=16)
    description = models.TextField(default="")
    avg_starttime = models.TimeField(default="12:00:00")
    avg_endtime = models.TimeField(default="15:00:00")
    avg_day_length = models.TimeField(default="05:00:00")
    free_on_monday = models.BooleanField(default=False)
    free_on_tuesday = models.BooleanField(default=False)
    free_on_wednesday = models.BooleanField(default=False)
    free_on_thursday = models.BooleanField(default=False)
    free_on_friday = models.BooleanField(default=False)

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

    # def compute_avg_starttime(self):
    #     starttime_sum = 0
    #     week = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
    #     instances = []
    #     for activity in self.activities.all():
    #         instances = instances + activity.get_instances_list()
        
    #     for day in week:
    #         t = activity.activity_instance_set.all().filter(
                
    #             day__exact=day
    #         ).order_by('starttime').first().starttime
    #         t_sec = day_start.hour*3600+day_start.minute*60
    #         starttime_sum = starttime_sum + t_sec
            
    # def compute_avg_endtime(self):

    # def compute_avg_day_length(self):

    # def find_free_days(self):

    # def generate_description(self):

class Term_Location(models.Model):
    term = models.CharField(max_length=16)
    location = models.CharField(max_length=32)