from django.contrib import admin
from .models import Workout, WorkoutPlan, WorkoutSession, MuscleGroup, WorkoutPlanItem, Set

class WorkoutPlanItemInline(admin.TabularInline):
    model = WorkoutPlanItem
    extra = 1

class SetInline(admin.TabularInline):
    model = Set
    extra = 1

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    list_filter = ['muscle_groups', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['muscle_groups']

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'difficulty', 'is_public', 'created_at']
    list_filter = ['difficulty', 'is_public', 'created_at']
    search_fields = ['name', 'description']
    inlines = [WorkoutPlanItemInline]

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'workout_plan', 'date', 'rating']
    list_filter = ['date', 'rating']
    search_fields = ['user__username', 'workout_plan__name']
    inlines = [SetInline]

@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ['workout_session', 'workout', 'weight_kg', 'reps', 'order']
    list_filter = ['workout']