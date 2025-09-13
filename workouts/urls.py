from django.urls import path

from . import views


app_name = 'workouts'
urlpatterns = [
    path('', views.index, name='index'),
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/create/', views.create_workout, name='create_workout'),
    path('plans/', views.workoutplan_list, name='workoutplan_list'),
    path('plans/<int:pk>/', views.workoutplan_detail, name='workoutplan_detail'),
    path('plans/create/', views.create_workoutplan, name='create_workoutplan'),
    path('session/start/', views.start_session, name='start_session'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
    path('register/', views.register, name='register'),
]