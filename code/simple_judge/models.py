from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField
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
    #question_content=models.JSONField('quiz_content')
    ifpassed=models.BooleanField('ifpassed')
    def __str__(self):
        return self.question_title

class Questiondict(models.Model):
    question_title=models.CharField(max_length=200)
    question_content=models.JSONField('quiz_content')
    question_id=IntegerField()
    def __str__(self):
        return self.question_title