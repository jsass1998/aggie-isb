from rest_framework import serializers
from .models import Course
from .models import Professor
from .models import Course_Prof
from .models import Activity
from .models import Section
from .models import Schedule
from .models import Activity_Instance

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'course_id',
            'title',
        )
        model = Course

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'dept',
            'office',
            'rate_my_prof',
        )
        model = Professor

class CourseProfSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'course',
            'professor',
            'percent_A',
            'percent_B',
            'percent_C',
            'percent_D',
            'percent_F',
            'percent_Q',
        )
        model = Course_Prof

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'term',
        )
        model = Activity

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'activity',
            'course_prof',
            'term',
            'section_num',
            'honors',
        )
        model = Section

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'user',
            'activities',
        )
        model = Schedule

class ActivityInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'activity',
            'location',
            'day',
            'starttime',
            'endtime',
        )
        model = Activity_Instance