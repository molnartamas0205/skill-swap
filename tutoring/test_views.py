from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import (
    Category,
    TargetAudience,
    TutoringService,
    ServiceAudience,
)

User = get_user_model()


class ViewTestsWithModels(TestCase):
    def setUp(self):
        # Initialize the test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='password123',
            username='testuser',
            full_name='Test User',
        )

        # Create categories
        self.category = Category.objects.create(name='Math')

        # Create target audiences
        self.high_school_audience = TargetAudience.objects.create(name='High School')
        self.college_audience = TargetAudience.objects.create(name='College')

        # Create a tutoring service
        self.tutoring_service = TutoringService.objects.create(
            user=self.user,
            category=self.category,
            title="Algebra Tutoring",
            description="Learn algebra with ease.",
            price=50.00,
        )

        # Create a service audience
        ServiceAudience.objects.create(
            tutoring_service=self.tutoring_service,
            target_audience=self.high_school_audience,
        )

        # URLs
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.logout_url = reverse('logout')
        self.tutors_url = reverse('tutors')
        self.create_advertisement_url = reverse('create_advertisement')

    def test_tutor_list_view(self):
        response = self.client.get(self.tutors_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Algebra Tutoring")

    def test_create_advertisement_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.post(self.create_advertisement_url, {
            'title': 'Geometry Tutoring',
            'description': 'Master geometry concepts.',
            'price': '60.00',
            'category': self.category.id,
            'target_audiences': [self.high_school_audience.id, self.college_audience.id],
        })
        self.assertRedirects(response, self.tutors_url)
        self.assertTrue(TutoringService.objects.filter(title='Geometry Tutoring').exists())

        # Check if audiences are linked
        new_service = TutoringService.objects.get(title='Geometry Tutoring')
        self.assertEqual(new_service.category, self.category)
        self.assertEqual(new_service.serviceaudience_set.count(), 2)

    def test_login_view(self):
        response = self.client.post(self.login_url, {
            'email': 'testuser@example.com',
            'password': 'password123',
        })
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(self.logout_url)
        self.assertRedirects(response, reverse('home'))

    def test_service_audience_relationship(self):
        # Test if the service audience relationship is correctly created
        service_audiences = ServiceAudience.objects.filter(tutoring_service=self.tutoring_service)
        self.assertEqual(service_audiences.count(), 1)
        self.assertEqual(service_audiences.first().target_audience, self.high_school_audience)
