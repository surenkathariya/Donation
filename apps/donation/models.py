
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # is_volunteer = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Donor(models.Model):
    Items=[
        ('Cloth','Cloth'),
        ('Food', 'Food'),
        ('Money','Money'),
        ('Others','Others'),
    ]
    Status=[
        ('Pending','Pending'),
        ('Accept','Accept'),
        ('Reject','Reject'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    userid=models.IntegerField(null=True)
    contact = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=300, null=True)
    userpic = models.FileField(upload_to='uploads/%Y/%m/%D', null=True)
    regdate = models.DateTimeField(auto_now_add=True)
    items=models.CharField(max_length=100, choices=Items, null=True)
    description = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=40, choices=Status,null=True, default='Pending')
    Receive=models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.email


