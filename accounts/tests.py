from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail


class AccountsTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse('workouts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="email"')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_theme_toggle_is_available_on_shared_layout(self):
        response = self.client.get(reverse('workouts:index'))
        self.assertContains(response, 'data-theme-toggle')
        self.assertContains(response, 'fittrack-theme')

    def test_login_page_links_to_password_reset(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, reverse('password_reset'))
        self.assertContains(response, "password-toggle")
        self.assertContains(response, "Show password")

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_sends_email(self):
        User.objects.create_user(
            username='reset-user',
            email='reset@example.com',
            password='old-password-123',
        )

        response = self.client.post(
            reverse('password_reset'),
            {'email': 'reset@example.com'},
        )

        self.assertRedirects(response, reverse('password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('reset-user', mail.outbox[0].body)
