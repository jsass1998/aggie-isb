from django.contrib import admin

from .models import Course
from .models import Professor
from .models import Course_Prof
from .models import Activity
from .models import Section
from .models import Schedule
from .models import Activity_Instance
from .models import Term_Location

admin.site.register(Course)
admin.site.register(Professor)
admin.site.register(Course_Prof)
admin.site.register(Activity)
admin.site.register(Section)
admin.site.register(Schedule)
admin.site.register(Activity_Instance)
admin.site.register(Term_Location)
