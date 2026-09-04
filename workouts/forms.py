from django import forms
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Workout, WorkoutPlan, WorkoutSession, Set


class StyledPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'email',
            'placeholder': 'you@example.com',
        })

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['name', 'description', 'muscle_groups', 'demonstration_video_url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'muscle_groups': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'demonstration_video_url': forms.URLInput(attrs={'class': 'form-control'}),
        }

class WorkoutPlanForm(forms.ModelForm):
    workouts = forms.ModelMultipleChoiceField(
        queryset=Workout.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text='Select workouts to include in this plan.'
    )

    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description', 'difficulty', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class WorkoutSessionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['workout_plan'].queryset = WorkoutPlan.objects.filter(
            Q(creator=user) | Q(is_public=True)
        ).distinct()

    class Meta:
        model = WorkoutSession
        fields = ['workout_plan', 'notes']
        widgets = {
            'workout_plan': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SetForm(forms.ModelForm):
    def __init__(self, session, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['workout'].queryset = Workout.objects.all()
        if session.workout_plan:
            self.fields['workout'].queryset = Workout.objects.filter(
                plans=session.workout_plan
            )

    class Meta:
        model = Set
        fields = ['workout', 'weight_kg', 'reps']
        widgets = {
            'workout': forms.Select(attrs={'class': 'form-select'}),
            'weight_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.25'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'autocomplete': 'email',
            'placeholder': 'you@example.com',
        }),
    )
    first_name = forms.CharField(max_length=30, required=False, label='First name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, label='Last name', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
