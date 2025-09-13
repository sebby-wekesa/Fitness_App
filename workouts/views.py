# workouts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import Workout, WorkoutPlan, WorkoutSession, Set
from .forms import WorkoutForm, WorkoutPlanForm, WorkoutSessionForm, SetForm

def index(request):
    public_plans = WorkoutPlan.objects.filter(is_public=True)[:5]
    recent_workouts = Workout.objects.all()[:5]
    return render(request, 'workouts/index.html', {
        'public_plans': public_plans,
        'recent_workouts': recent_workouts
    })

def workout_list(request):
    workouts = Workout.objects.all()
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})

def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)
    return render(request, 'workouts/workout_detail.html', {'workout': workout})

def workoutplan_list(request):
    plans = WorkoutPlan.objects.filter(is_public=True)
    return render(request, 'workouts/workoutplan_list.html', {'plans': plans})

def workoutplan_detail(request, pk):
    plan = get_object_or_404(WorkoutPlan, pk=pk)
    return render(request, 'workouts/workoutplan_detail.html', {'plan': plan})

@login_required
def create_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.created_by = request.user
            workout.save()
            form.save_m2m()  # Save many-to-many data
            return redirect('workout_detail', pk=workout.pk)
    else:
        form = WorkoutForm()
    return render(request, 'workouts/create_workout.html', {'form': form})

@login_required
def create_workoutplan(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.creator = request.user
            plan.save()
            return redirect('workoutplan_detail', pk=plan.pk)
    else:
        form = WorkoutPlanForm()
    return render(request, 'workouts/create_workoutplan.html', {'form': form})

@login_required
def start_session(request):
    if request.method == 'POST':
        form = WorkoutSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()
            return redirect('session_detail', pk=session.pk)
    else:
        form = WorkoutSessionForm()
    return render(request, 'workouts/start_session.html', {'form': form})

@login_required
def session_detail(request, pk):
    session = get_object_or_404(WorkoutSession, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SetForm(request.POST)
        if form.is_valid():
            set_instance = form.save(commit=False)
            set_instance.workout_session = session
            set_instance.order = session.sets.count() + 1
            set_instance.save()
            return redirect('session_detail', pk=session.pk)
    else:
        form = SetForm()
    return render(request, 'workouts/session_detail.html', {
        'session': session,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'workouts/registration/register.html', {'form': form})