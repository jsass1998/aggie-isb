from rest_framework import serializers
from .models import Course
from .models import Professor
from .models import Course_Prof
from .models import Activity
from .models import Section
from .models import Schedule
from .models import Activity_Instance
from .models import Term_Location
from users.models import User

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
            'rating_class',
            'overall_rating',
            'num_ratings',
            'rmp_link',
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
            'activity',
            'location',
            'day',
            'starttime',
            'endtime',
        )
        model = Activity_Instance

class SectionSerializer(serializers.ModelSerializer):
    course_prof = CourseProfSerializer()

    class Meta:
        fields = (
            'activity',
            'course_prof',
            'section_num',
            'crn',
            'credit_hours',
            'honors',
            'web',
            'total_seats',
            'seats_taken',
            'interested_students',
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
            'term',
            #'description',
        )
        model = Schedule

class TermLocationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'term',
            'location',
        )
        model = Term_Location

class AppUserSerializer(serializers.ModelSerializer):
    schedule_set = ScheduleSerializer(many=True)

    class Meta:
        fields = (
            'id',
            'email',
            'is_staff',
            'is_active',
            'last_login',
            'schedule_set',
        )
        model = User
