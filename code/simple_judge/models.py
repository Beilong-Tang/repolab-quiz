from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#from ..utils.AssignQuestionWeek import 
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name=models.CharField(max_length=200)
    student_id=models.IntegerField(default=0)
    def __str__(self):
        return self.student_name

class Question(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    question_title=models.CharField(max_length=50)
    question_id=models.IntegerField(default=0)
    ifpassed=models.BooleanField('ifpassed',default=False)
    pub_date=models.DateTimeField('date published', default=datetime.datetime.strptime('2022-7-13 23:59','%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8))))
    due_date=models.DateTimeField('date due', default=datetime.datetime.strptime('2022-7-14 23:59','%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8))))
    logx=models.TextField()
    submission_times=models.IntegerField(default=5)
    def __str__(self):
        return self.question_title

class Questiondict(models.Model):
    question_type=models.CharField(max_length=200)
    question_title=models.CharField(max_length=200)
    question_content=models.JSONField('quiz_content')
    question_id=models.IntegerField(default=0)
    question_level=models.IntegerField(default=0)
    question_week=models.IntegerField(default=0)
    def __str__(self):
        return self.question_title

