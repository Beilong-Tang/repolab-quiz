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
    question_title=models.CharField(max_length=200)
    #question_content=models.JSONField('quiz_content')
    ifpassed=models.BooleanField('ifpassed')
    pub_date=models.DateTimeField('date published', default=timezone.now())
    due_date=models.DateTimeField('date due', default=timezone.now())
    submission_times=models.IntegerField(default=2)
    #level=0
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


## Here are model managers like add or sth.
def test():
    for q in Questiondict.objects.all():
        if q.question_title=="chap01_new_sec-1.1_quiz.0.Programming.in.Java.qz.blank":
            q.question_week=7
            q.save()