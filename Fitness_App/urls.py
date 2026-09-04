"""
URL configuration for Fitness_App project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Fitness_App/urls.py
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from workouts.forms import StyledPasswordResetForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('workouts.urls', namespace='workouts')),  # Add namespace here
    path('login/', auth_views.LoginView.as_view(template_name='workouts/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            form_class=StyledPasswordResetForm,
            template_name='workouts/registration/password_reset_form.html',
            email_template_name='workouts/registration/password_reset_email.html',
            subject_template_name='workouts/registration/password_reset_subject.txt',
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='workouts/registration/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='workouts/registration/password_reset_confirm.html',
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='workouts/registration/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
