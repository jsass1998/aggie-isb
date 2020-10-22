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
    course = CourseSerializer()
    professor = ProfessorSerializer()
    
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

class ActivityInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'location',
            'day',
            'starttime',
            'endtime',
        )
        model = Activity_Instance

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'course_prof',
            'section_num',
            'honors',
        )
        model = Section

class ActivitySerializer(serializers.ModelSerializer):
    activity_instance_set = ActivityInstanceSerializer(many=True)
    section = SectionSerializer()
    
    class Meta:
        fields = (
            'id',
            'title',
            'term',
            'section',
            'activity_instance_set',
        )
        model = Activity
    
    def create(self, validated_data):
        section_data = validated_data.pop('section')
        instances_data = validated_data.pop('activity_instance_set')
        activity = Activity.objects.create(**validated_data)
        Section.objects.create(activity=activity, **section_data)
        for instance_data in instances_data:
            Activity_Instance.objects.create(activity=activity, **instance_data)
        return activity

class ScheduleSerializer(serializers.ModelSerializer):
    activities = ActivitySerializer(many=True)
    
    class Meta:
        fields = (
            'id',
            'user',
            'activities',
        )
        model = Schedule