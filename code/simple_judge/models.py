from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#from ..utils.AssignQuestionWeek import 
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name=models.CharField(max_length=50)
    student_id=models.IntegerField(default=0)
    student_netid=models.CharField(max_length=8)
    question_due_dict=models.JSONField(default={'week1':['2022-7-29 6:00','2022-7-29 23:59']})
    online_time = models.DateTimeField(default=datetime.datetime.strptime('2022-7-26 6:00','%Y-%m-%d %H:%M'))
    offline_time = models.DateTimeField(default=datetime.datetime.strptime('2022-7-26 6:30','%Y-%m-%d %H:%M'))
    def __str__(self):
        return self.student_name

class Question(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    question_title=models.CharField(max_length=50)
    question_id=models.IntegerField(default=0)
    ifpassed=models.BooleanField('ifpassed',default=False)
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

