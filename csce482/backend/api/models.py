from django.db import models

class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)

    def __str__(self):
        return "Course: %s" % self.course_id

class Professor(models.Model):
    name = models.CharField(max_length=50)
    dept = models.CharField(max_length=50)
    office = models.CharField(max_length=20)
    rate_my_prof = models.CharField(max_length=100, null=True)

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
        s="Activity "+str(self.id)+": "+self.title+", "+self.term
        return s

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
    honors = models.BooleanField()

    class Meta:
        unique_together = ('course_prof', 'term', 'section_num')

    def __str__(self):
        return "Section: "+self.activity.title+", "+self.term

class Schedule(models.Model):
    #Many Schedules can be associated with a User
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE
    )
    #A schedule can have many Activities
    #An Activity can be part of many Schedules
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        s=str(self.id)+": "+str(self.user)
        s=s+" ("+str(self.activities.count())+" activities)"
        return s

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