from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet)
router.register(r'professors', views.ProfessorViewSet)
router.register(r'course_profs', views.CourseProfViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'activity_instances', views.ActivityInstanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include(
        'rest_framework.urls',
        namespace='rest_framework'
    )),
    #path('list/', views.ListSchedule.as_view()),
    #path('<int:pk>/', views.DetailSchedule.as_view()),
]