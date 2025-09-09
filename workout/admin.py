from django.contrib import admin
from .models import Workout, WorkoutPlan, WorkoutSession, MuscleGroup

class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

class WorkoutAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "muscle_group", "demonstration_video_url")

admin.site.register(MuscleGroup, MuscleGroupAdmin)
admin.site.register(Workout)
admin.site.register(WorkoutPlan)
admin.site.register(WorkoutSession)