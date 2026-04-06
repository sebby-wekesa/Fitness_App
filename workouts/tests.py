from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MuscleGroup, Workout, WorkoutPlan


class WorkoutPlanTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.muscle_group = MuscleGroup.objects.create(name='Legs')
        self.workout = Workout.objects.create(
            name='Squat',
            description='Lower body exercise',
            created_by=self.user,
        )
        self.workout.muscle_groups.add(self.muscle_group)

    def test_create_workout_plan_creates_plan_items(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(
            reverse('workouts:create_workoutplan'),
            {
                'name': 'Leg Day',
                'description': 'A simple leg workout plan.',
                'difficulty': 'B',
                'is_public': 'on',
                'workouts': [self.workout.pk],
            }
        )
        self.assertEqual(response.status_code, 302)
        plan = WorkoutPlan.objects.get(name='Leg Day')
        self.assertEqual(plan.creator, self.user)
        self.assertEqual(plan.items.count(), 1)
        self.assertEqual(plan.items.first().workout, self.workout)

    def test_private_plan_detail_only_owner(self):
        private_plan = WorkoutPlan.objects.create(
            name='Private Plan',
            description='Secret routine',
            creator=self.other_user,
            difficulty='I',
            is_public=False,
        )
        response = self.client.get(reverse('workouts:workoutplan_detail', args=[private_plan.pk]))
        self.assertEqual(response.status_code, 404)
        self.client.login(username='otheruser', password='password')
        response = self.client.get(reverse('workouts:workoutplan_detail', args=[private_plan.pk]))
        self.assertEqual(response.status_code, 200)
