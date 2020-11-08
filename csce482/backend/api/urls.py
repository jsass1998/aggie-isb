from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course-list')
router.register(r'professors', views.ProfessorViewSet)
router.register(r'course_profs', views.CourseProfViewSet)
router.register(r'activities', views.ActivityViewSet, basename='activity-list')
router.register(r'sections', views.SectionViewSet)
router.register(r'schedules', views.ScheduleViewSet)
router.register(r'activity_instances', views.ActivityInstanceViewSet)
router.register(r'term_locations', views.TermLocationViewSet)
router.register(r'users', views.AppUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate_schedules/', views.GenerateSchedule.as_view())
    #path('api-auth/', include(
    #    'rest_framework.urls',
    #    namespace='rest_framework'
    #)),
    #path('list/', views.ListSchedule.as_view()),
    #path('<int:pk>/', views.DetailSchedule.as_view()),
]