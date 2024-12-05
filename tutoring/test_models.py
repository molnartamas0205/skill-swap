from django.test import TestCase
from .models import (
    CustomUser,
    Category,
    TargetAudience,
    TutoringService,
    ServiceAudience,
)
from django.db.utils import IntegrityError

class CustomUserModelTests(TestCase):
    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="password123",
            full_name="Test User",
            username="testuser"
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.full_name, "Test User")

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com",
            password="admin123",
            full_name="Admin User",
        )
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.username, "admin")

    def test_user_string_representation(self):
        user = CustomUser.objects.create_user(
            email="user@example.com",
            password="password123",
            full_name="Sample User",
            username="sampleuser"
        )
        self.assertEqual(str(user), "sampleuser")

    def test_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email=None, 
                password="password123", 
                full_name="Test User"
            )

class CategoryModelTests(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Math")
        self.assertEqual(category.name, "Math")
        self.assertIsNone(category.parent)

    def test_category_with_parent(self):
        parent_category = Category.objects.create(name="Science")
        child_category = Category.objects.create(name="Physics", parent=parent_category)
        self.assertEqual(child_category.parent, parent_category)
        self.assertEqual(child_category.name, "Physics")

    def test_category_string_representation(self):
        category = Category.objects.create(name="Programming")
        self.assertEqual(str(category), "Programming")

class TargetAudienceModelTests(TestCase):
    def test_create_target_audience(self):
        audience = TargetAudience.objects.create(name="High School")
        self.assertEqual(audience.name, "High School")

    def test_target_audience_string_representation(self):
        audience = TargetAudience.objects.create(name="College Students")
        self.assertEqual(str(audience), "College Students")

class TutoringServiceModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="tutor@example.com",
            password="password123",
            full_name="Tutor Name",
            username="tutor"
        )
        self.category = Category.objects.create(name="Math")

    def test_create_tutoring_service(self):
        service = TutoringService.objects.create(
            user=self.user,
            category=self.category,
            title="Algebra Tutoring",
            description="Learn algebra with an expert.",
            price=50.00
        )
        self.assertEqual(service.title, "Algebra Tutoring")
        self.assertEqual(service.category, self.category)
        self.assertEqual(service.user, self.user)
        self.assertEqual(service.price, 50.00)
        self.assertTrue(service.available)

    def test_tutoring_service_string_representation(self):
        service = TutoringService.objects.create(
            user=self.user,
            title="Physics Tutoring",
            price=70.00
        )
        self.assertEqual(str(service), "Physics Tutoring")

class ServiceAudienceModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="tutor@example.com",
            password="password123",
            full_name="Tutor Name",
            username="tutor"
        )
        self.category = Category.objects.create(name="Math")
        self.service = TutoringService.objects.create(
            user=self.user,
            category=self.category,
            title="Geometry Tutoring",
            price=60.00
        )
        self.audience = TargetAudience.objects.create(name="College Students")

    def test_create_service_audience(self):
        service_audience = ServiceAudience.objects.create(
            tutoring_service=self.service,
            target_audience=self.audience
        )
        self.assertEqual(service_audience.tutoring_service, self.service)
        self.assertEqual(service_audience.target_audience, self.audience)

    def test_service_audience_string_representation(self):
        service_audience = ServiceAudience.objects.create(
            tutoring_service=self.service,
            target_audience=self.audience
        )
        self.assertEqual(str(service_audience), "Geometry Tutoring - College Students")

    def test_unique_service_audience(self):
        ServiceAudience.objects.create(
            tutoring_service=self.service,
            target_audience=self.audience
        )
        with self.assertRaises(IntegrityError):
            ServiceAudience.objects.create(
                tutoring_service=self.service,
                target_audience=self.audience
            )
