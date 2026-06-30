from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.utils import timezone
from .models import Workout, WorkoutPlan, WorkoutPlanItem, WorkoutSession, Set
from .forms import WorkoutForm, WorkoutPlanForm, WorkoutSessionForm, SetForm, CustomUserCreationForm


def index(request):
    public_plans = WorkoutPlan.objects.filter(is_public=True)[:5]
    recent_workouts = Workout.objects.order_by('-created_at')[:5]
    return render(request, 'workouts/index.html', {
        'public_plans': public_plans,
        'recent_workouts': recent_workouts
    })


def equipment(request):
    return render(request, 'workouts/equipment.html')


def coaching(request):
    return render(request, 'workouts/coaching.html')


def members(request):
    return render(request, 'workouts/members.html')


def facilities(request):
    return render(request, 'workouts/facilities.html')


def free_trial(request):
    return render(request, 'workouts/free_trial.html')


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
    plans = WorkoutPlan.objects.filter(is_public=True)
    if request.user.is_authenticated:
        plans = plans | WorkoutPlan.objects.filter(creator=request.user)
    plan = get_object_or_404(plans.distinct(), pk=pk)
    return render(request, 'workouts/workoutplan_detail.html', {'plan': plan})


@login_required
def create_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.created_by = request.user
            workout.save()
            form.save_m2m()
            return redirect('workouts:workout_detail', pk=workout.pk)
    else:
        form = WorkoutForm()
    return render(request, 'workouts/create_workout.html', {'form': form})


@login_required
def create_workoutplan(request):
    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            workouts = form.cleaned_data.get('workouts')
            plan = form.save(commit=False)
            plan.creator = request.user
            plan.save()
            for order, workout in enumerate(workouts, start=1):
                WorkoutPlanItem.objects.create(workout_plan=plan, workout=workout, order=order)
            return redirect('workouts:workoutplan_detail', pk=plan.pk)
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
            return redirect('workouts:session_detail', pk=session.pk)
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
            return redirect('workouts:session_detail', pk=session.pk)
    else:
        form = SetForm()
    return render(request, 'workouts/session_detail.html', {
        'session': session,
        'form': form
    })


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('workouts:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'workouts/registration/register.html', {'form': form})
