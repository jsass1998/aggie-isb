from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView

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

from .generate_schedules import generate_schedules

#class ListSchedule(generics.ListCreateAPIView):
#    queryset = Schedule.objects.all()
#    serializer_class = ScheduleSerializer

#class DetailSchedule(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Schedule.objects.all()
#    serializer_class = ScheduleSerializer

class CourseViewSet(viewsets.ModelViewSet):
    #queryset = Course.objects.all().order_by('course_id')
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all().order_by('id')
        term_param = self.request.query_params.get('term', None)
        if (term_param is not None):
            queryset = Course.objects.all().get(term=term_param)
            #queryset = queryset.filter(
                #section__isnull = False,
                #term__icontains = term_param,
                #section__course_prof__course__course_id__icontains = course_param
            #)
        return queryset

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
            queryset = Course.objects.get(course_id__icontains=course_param).get_sections(term_param)
            #queryset = queryset.filter(
                #section__isnull = False,
                #term__icontains = term_param,
                #section__course_prof__course__course_id__icontains = course_param
            #)
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

class GenerateSchedule(APIView):
    def post(self, request):
        user_id = request.data['user_id']
        user = User.objects.all().get(id = user_id)
        term = request.data['term']
        course_ids = request.data['courses']
        courses=[]
        for course_id in course_ids:
            course = Course.objects.all().get(course_id=course_id)
            courses.append(course)
        blocked_times = tuple(request.data['blocked_times'])
        schedules = generate_schedules(user, term, courses, blocked_times)
        return JsonResponse(schedules)