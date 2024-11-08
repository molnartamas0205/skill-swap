from django.db import models


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    path = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class TargetAudience(models.Model):
    name = models.CharField(max_length=255)

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

    def __str__(self):
        return self.title


# ServiceAudience model (Many-to-Many relationship between TutoringService and TargetAudience)
class ServiceAudience(models.Model):
    tutoring_service = models.ForeignKey(TutoringService, on_delete=models.CASCADE)
    target_audience = models.ForeignKey(TargetAudience, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tutoring_service', 'target_audience')

    def __str__(self):
        return f"{self.tutoring_service.title} - {self.target_audience.name}"


