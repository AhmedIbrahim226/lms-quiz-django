from django.contrib import admin
from .models import (
    Post, Course, Material,
    TaskInstructor, Quiz,
    InstructorSchedule, 
    StudentSchedule,
    Schedule
)

admin.site.register(Post)
admin.site.register(Course)
admin.site.register(Material)
admin.site.register(TaskInstructor)
admin.site.register(Quiz)
admin.site.register(InstructorSchedule)
admin.site.register(StudentSchedule)
admin.site.register(Schedule)
