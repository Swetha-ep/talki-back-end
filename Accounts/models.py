from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff ", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_role", 'admin')

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)

ROLE_CHOICES = [
    ('user', 'User'),
    ('trainer', 'Trainer'),
    ('admin', 'Admin'),
]

LEVEL_CHOICES = [
    ('beginner', 'beginner'),
    ('intermediate', 'intermediate'),
    ('advanced', 'advanced'),
]

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    user_role = models.CharField(max_length=10,default='user', choices=ROLE_CHOICES)
    is_vip = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True)
    is_google = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
 
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    

class TutorApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField()  
    about_me = models.TextField()
    teaching_style = models.TextField()
    work_experience = models.TextField()
    education = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'pending'), ('accepted', 'accepted'), ('declined', 'declined')], default='pending')

    def __str__(self):
        return self.name

