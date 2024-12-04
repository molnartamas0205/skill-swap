from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
import pickle


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, full_name, username=None, **extra_fields):
        """
        Creates and returns a user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        

        email = self.normalize_email(email)
        
        user = self.model(username=username,
            email=email,
            full_name=full_name,
            **extra_fields
        )
        
        user.save(using=self._db) 
        user.set_password(password)  # Hashes the password before saving
        user.save()
        return user
    
    def create_superuser(self, email, password=None, full_name=None, username=None, **extra_fields):
        """Create and return a superuser with an email."""
        extra_fields.setdefault('is_staff', True)
        

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        

        extra_fields.setdefault('username', email.split('@')[0])

        return self.create_user(email, username, password, **extra_fields)

    
    

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = None
    password = None
    
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # The field used for authentication
    REQUIRED_FIELDS = []
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
    
    def set_password(self, raw_password):
        """
        The password is saved for hashing and encryption in the password_hash field.
        """
        self.password_hash = make_password(raw_password)  
 

    def check_password(self, raw_password):
        """
        Checks if the raw password matches the stored hashed password.
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password_hash)
    
     # Django adminisztrációhoz szükséges metódusok
    def has_perm(self, perm, obj=None):
        """
        Egyéni engedélyeket kezel.
        """
        return True  # A felhasználónak minden engedély megadható, vagy testre szabható.

    def has_module_perms(self, app_label):
        """
        Meghatározza, hogy a felhasználónak van-e engedélye az adott modulhoz.
        """
        return True  # Minden alkalmazáshoz engedélyezve van.
    
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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


