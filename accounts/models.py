from email.policy import default
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django_base64field.fields import Base64Field


class UserProfile(AbstractUser):
    role = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    user_image = Base64Field(max_length=900000, blank=True, null=False)

