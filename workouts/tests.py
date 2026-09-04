from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import MuscleGroup, Workout, WorkoutPlan, WorkoutPlanItem, WorkoutSession


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

    def test_start_session_only_lists_public_and_owned_plans(self):
        private_plan = WorkoutPlan.objects.create(
            name='Other Private Plan',
            description='Not available to this user',
            creator=self.other_user,
            difficulty='I',
        )
        public_plan = WorkoutPlan.objects.create(
            name='Public Plan',
            description='Available to everyone',
            creator=self.other_user,
            difficulty='B',
            is_public=True,
        )
        own_plan = WorkoutPlan.objects.create(
            name='My Plan',
            description='Available to me',
            creator=self.user,
            difficulty='B',
        )

        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('workouts:start_session'))
        plan_queryset = response.context['form'].fields['workout_plan'].queryset

        self.assertNotIn(private_plan, plan_queryset)
        self.assertIn(public_plan, plan_queryset)
        self.assertIn(own_plan, plan_queryset)

    def test_session_only_accepts_workouts_from_selected_plan(self):
        plan = WorkoutPlan.objects.create(
            name='Leg Day',
            description='Lower body session',
            creator=self.user,
            difficulty='B',
        )
        WorkoutPlanItem.objects.create(workout_plan=plan, workout=self.workout, order=1)
        other_workout = Workout.objects.create(
            name='Bench Press',
            description='Upper body exercise',
            created_by=self.user,
        )
        session = WorkoutSession.objects.create(user=self.user, workout_plan=plan)

        self.client.login(username='testuser', password='password')
        response = self.client.post(
            reverse('workouts:session_detail', args=[session.pk]),
            {'workout': other_workout.pk, 'weight_kg': '80', 'reps': '5'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(session.sets.count(), 0)

    def test_member_dashboard_uses_live_stats(self):
        WorkoutSession.objects.create(user=self.user)
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('workouts:index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['my_session_count'], 1)
        self.assertEqual(response.context['my_plan_count'], 0)
        self.assertEqual(response.context['my_workout_count'], 1)
