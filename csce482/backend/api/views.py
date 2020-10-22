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
from users.models import User

from .serializers import CourseSerializer
from .serializers import ProfessorSerializer
from .serializers import CourseProfSerializer
from .serializers import ActivitySerializer
from .serializers import SectionSerializer
from .serializers import ScheduleSerializer
from .serializers import ActivityInstanceSerializer
from .serializers import AppUserSerializer

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
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        queryset = Activity.objects.all().order_by('id')
        course_param = self.request.query_params.get('course', None)
        term_param = self.request.query_params.get('term', None)
        if (course_param is not None):
            queryset = queryset.filter(
                section__isnull = False,
                term__icontains = term_param,
                section__course_prof__course__course_id__icontains = course_param
            )
        return queryset

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all().order_by('activity')
    serializer_class = SectionSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('id')
    serializer_class = ScheduleSerializer

class ActivityInstanceViewSet(viewsets.ModelViewSet):
    queryset = Activity_Instance.objects.all().order_by('id')
    serializer_class = ActivityInstanceSerializer

class AppUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = AppUserSerializer
