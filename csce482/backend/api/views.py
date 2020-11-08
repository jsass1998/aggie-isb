from django.http import JsonResponse
from django.http import HttpResponse
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
        queryset = Course.objects.all().order_by('course_id')
        term_param = self.request.query_params.get('term', None)
        if (term_param is not None):
            sections_qset = Section.objects.all().filter(
                term__exact = term_param
            ).select_related('course_prof__course')
            course_list = [section.course_prof.course.course_id for section in sections_qset]
            queryset = Course.objects.filter(course_id__in=course_list).distinct()
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
        # Extract function parameters from request
        user_id = request.data['user_id']
        user = User.objects.all().get(id = user_id)
        term = request.data['term']
        course_ids = request.data['courses']
        course_qset = Course.objects.all().filter(
            course_id__in=course_ids
        )
        courses=[course for course in course_qset]
        blocked_times = request.data['blocked_times']
        
        # Generate list of schedules
        schedule_list = generate_schedules(user, term, courses, blocked_times)
        
        # Convert list to queryset and then serialize
        schedule_ids = [schedule.id for schedule in schedule_list]
        schedules = Schedule.objects.all().filter(
            id__in = schedule_ids
        )
        
        serializer = ScheduleSerializer(schedules, many=True)

        # #Return dict of serialized 
        # schedules_dict = {
        #     "schedules": serializer.data
        # }

        return HttpResponse(serializer.data)
        #return JsonResponse(schedules_dict)