from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class MuscleGroup(models.Model):
    name = models.CharField(max_length=100) #e.g chest, bisept, legs and back
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    muscle_group = models.ManyToManyField(MuscleGroup)
    demonstration_video_url = models.URLField(blank=True, null=True)# a link to youtube video
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
    
class WorkoutPlan(models.Model):
    DIFFICULTY_CHOICES = [
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
    ]
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_plans')
    description = models.TextField()
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES, default='B')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class WorkoutSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout_plan = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s session on {self.date}"

class Set(models.Model):
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Workout, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) # Allows for bodyweight exercises
    reps = models.PositiveIntegerField()
    order = models.PositiveIntegerField() # To track the order of exercises

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.name} - {self.reps} reps ({self.weight_kg} kg)"