from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets

from .models import Course
from .models import Professor
from .models import Course_Prof
from .models import Activity
from .models import Section
from .models import Schedule
from .models import Activity_Instance

from .serializers import CourseSerializer
from .serializers import ProfessorSerializer
from .serializers import CourseProfSerializer
from .serializers import ActivitySerializer
from .serializers import SectionSerializer
from .serializers import ScheduleSerializer
from .serializers import ActivityInstanceSerializer

#class ListSchedule(generics.ListCreateAPIView):
#    queryset = Schedule.objects.all()
#    serializer_class = ScheduleSerializer

#class DetailSchedule(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Schedule.objects.all()
#    serializer_class = ScheduleSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('id')
    serializer_class = ProfessorSerializer

class CourseProfViewSet(viewsets.ModelViewSet):
    queryset = Course_Prof.objects.all().order_by('id')
    serializer_class = CourseProfSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all().order_by('id')
    serializer_class = ActivitySerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by('activity')
    serializer_class = SectionSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('id')
    serializer_class = ScheduleSerializer

class ActivityInstanceViewSet(viewsets.ModelViewSet):
    queryset = Activity_Instance.objects.all().order_by('id')
    serializer_class = ActivityInstanceSerializer

