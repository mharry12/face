from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ROLE.ADMIN)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class ROLE(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CREATOR = 'CREATOR', 'Creator'
        MANAGER = 'MANAGER', 'Manager'
        SUPPORT = 'SUPPORT', 'Support'
        CUSTOMER = 'CUSTOMER', 'Customer'

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    is_creator = models.BooleanField(default=False)

    # ✅ Only one is_staff field
    is_staff = models.BooleanField(default=False)

    # ✅ Keep is_active, but only once
    is_active = models.BooleanField(default=True)

    # ✅ Role field
    role = models.CharField(max_length=20, choices=ROLE.choices, default=ROLE.CUSTOMER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email




from django.db import models
from django.conf import settings  # ✅ correct

class ImagePost(models.Model):  # You can rename the model if desired
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/')  # Changed from FileField to ImageField
    views = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# models.py
from django.db import models

class VisitorTracking(models.Model):
    content_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    action = models.CharField(max_length=50, blank=True)  # e.g., 'page_view', 'play_button_click'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content_id} - {self.ip_address} - {self.created_at}"