# workouts/forms.py
from django import forms
from .models import Workout, WorkoutPlan, WorkoutSession, Set

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'muscle_groups', 'demonstration_video_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description', 'difficulty', 'is_public']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class WorkoutSessionForm(forms.ModelForm):
    class Meta:
        model = WorkoutSession
        fields = ['workout_plan', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

class SetForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['workout', 'weight_kg', 'reps']