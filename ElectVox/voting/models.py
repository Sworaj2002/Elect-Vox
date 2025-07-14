from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)

class User(AbstractBaseUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name']
    
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    age = models.IntegerField(null=True, blank=True)
    aadhar = models.CharField(max_length=12, null=True, blank=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)  # election officers
    
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.date_of_birth:
            self.age = self.calculate_age(self.date_of_birth)
        super(User, self).save(*args, **kwargs)

    def calculate_age(self, dob):
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def __str__(self):
        return self.email


class RegisterCandidate(models.Model):
    full_name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='candidate_photos/')  # Use ImageField to store image files
    aadhar_number = models.CharField(max_length=20)
    voter_id = models.CharField(max_length=50)
    manifesto = models.TextField()
    supporters_names = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
