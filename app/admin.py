from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Questionset)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Exams_Results)
admin.site.register(CustomUser)

admin.site.register(Exam)
