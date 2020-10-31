from django.db import models

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)

    def __str__(self):
        return "Course: %s" % self.course_id

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
    term = models.CharField(max_length=20)

    def __str__(self):
        return self.title+" - "+self.term
    
    def conflicts_with(self, other_activity):
        for a in self.activity_instance_set:
            for b in other_activity.activity_instance_set:
                if a.conflicts_with(b):
                    return True
        return False

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

    term = models.CharField(max_length=20)
    section_num = models.IntegerField()
    crn = models.IntegerField()
    credit_hours = models.IntegerField()
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

class Schedule(models.Model):
    #Many Schedules can be associated with a User
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    #A schedule can have many Activities
    #An Activity can be part of many Schedules
    activities = models.ManyToManyField(Activity)
    #term = models.CharField(max_length=20)

    def __str__(self):
        s=str(self.id)+": "+str(self.user)
        s=s+" ("+str(self.activities.count())+" activities)"
        return s
    
    def conflicts_with(self, activity):
        for a in self.activities:
            if a.conflicts_with(activity):
                return True
        return False

    def get_sections(self):
        return self.activities.all().filter(section__isnull = False)

class Activity_Instance(models.Model):
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE
    )
    location = models.CharField(max_length=50)
    day = models.CharField(max_length=10)
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
