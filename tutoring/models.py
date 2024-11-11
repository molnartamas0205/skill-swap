from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and returns a user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password before saving
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)  # Ensures 'is_staff' is True for superusers
        return self.create_user(email, password, **extra_fields)  # Calls create_user to create the superuser

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'  # The field used for authentication
    REQUIRED_FIELDS = ['full_name']
    class Meta:
        db_table = "users"
    
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False
    
    @property
    def is_authenticated(self):
        """
        Return True for authenticated users. 
        """
        return True
    
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    path = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = "categories"
    
    def __str__(self):
        return self.name


class TargetAudience(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "target_audiences"

    def __str__(self):
        return self.name


class TutoringService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tutoring_services"

    def __str__(self):
        return self.title


# ServiceAudience model (Many-to-Many relationship between TutoringService and TargetAudience)
class ServiceAudience(models.Model):
    tutoring_service = models.ForeignKey(TutoringService, on_delete=models.CASCADE)
    target_audience = models.ForeignKey(TargetAudience, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tutoring_service', 'target_audience')
        db_table = "service_audiences"

    def __str__(self):
        return f"{self.tutoring_service.title} - {self.target_audience.name}"


