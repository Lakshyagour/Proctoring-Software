from django.db import models
from django_base64field.fields import Base64Field


class ProctoringLog(models.Model):
    student_id = models.CharField(max_length=100)
    test_id = models.CharField(max_length=100)
    # flag_type = models.CharField(max_length=100)
    flag = models.CharField(max_length=100)
    image = Base64Field(max_length=900000)
    timestamp = models.TimeField(auto_now_add=True)

# Create your models here.


