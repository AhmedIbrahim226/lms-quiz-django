from schedule.models import (
    Post, Material, MaterialVideo,
    TaskInstructor, TaskStudent,
    InstructorSchedule, StudentSchedule,
    Schedule, Course
)

from rest_framework import serializers

class InstructorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructorSchedule
        # fields = ['instructor_schedule_name', 'company_name']
        fields = '__all__'

class GetCourse(serializers.ModelSerializer):
    class Meta:
        model = Course
        # fields = ['course_name', 'company_name', 'created_on']
        fields = '__all__'

class GetMaterialSlide(serializers.ModelSerializer):
    class Meta:
        model = Material
        # fields = ['material_name', 'Schedule_name', 'slide', 'company_name', 'created_on']
        fields = '__all__'
class GetMaterialVideo(serializers.ModelSerializer):
    class Meta:
        model = MaterialVideo
        # fields = ['material_name', 'Schedule_name', 'lecture_video', 'company_name', 'created_on']
        fields = '__all__'

class GetTaskInstructor(serializers.ModelSerializer):
    class Meta:
        model = TaskInstructor
        # fields = ['id', 'task_name', 'task_file', 'created_on']
        fields = '__all__'
