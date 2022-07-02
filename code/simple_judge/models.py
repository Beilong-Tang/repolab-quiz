from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name=models.CharField(max_length=200)
    student_id=models.IntegerField(default=0)
    def __str__(self):
        return self.student_name

class Question(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    question_title=models.CharField(max_length=200)
    question_content=models.CharField(max_length=200)
    def __str__(self):
        return self.question_title