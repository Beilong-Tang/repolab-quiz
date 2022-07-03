from urllib.request import HTTPRedirectHandler
from django.shortcuts import render
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.contrib.auth.models import User

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, models, logout
from django.contrib.auth import views
from django.views import generic

from simple_judge.models import Student, Question
import quiz.utils as ut
# Create your views here.

def checkuser(username,user_id):
    user_web = User.objects.get(pk=user_id)
    if (username!=user_web.username):
        return False
    return True

def index(request):
    return HttpResponse("HelloThere!")

def student_user(user_id):

    student=Student.objects.get(student_id=user_id)
    return student


def userface(request,user_id):
    if checkuser(request.user.username , user_id) !=True:
       return HttpResponse("You are not allowed to See the Page") 
    student=Student.objects.get(student_id=user_id)
    context={}
    context['user_id']=user_id
    question_sets=student.question_set.filter(ifpassed=False)
    context['quiz_title']=[question.question_content.get('description').lstrip('\n')[0:question.question_content.get('description').lstrip('\n').index('\n')].replace('#',"") for question in question_sets]
    context['question_title'] = [question.question_title for question in question_sets]
    context['quizes']={}
    for i in range (0,len(context['quiz_title'])):
        context['quizes'][context['quiz_title'][i]]=context['question_title'][i]
    return render(request, 'quiz/problems.html', context)

def quiz(request,user_id,question_title):
    if checkuser(request.user.username,user_id)!=True:
        return HttpResponse("You are not allowed to See the Page")
    student_current=student_user(user_id)
    quiz=student_current.question_set.get(question_title=question_title)

    context={}
    context['user_id']=user_id
    context['question_title']=question_title
    quiz_description=quiz.question_content.get('description').split('\n')
    context['quiz_description']=quiz_description
    

    return render(request, 'quiz/quiz.html', context)
 
def check(request, user_id, question_title):
    if checkuser(request.user.username,user_id)!=True:
        return HttpResponse("You are not allowed to See the Page")
    student_current=student_user(user_id)
    quiz=student_current.question_set.get(question_title=question_title)

    if request.method=='POST':
        answer=request.POST['answer'].split(' ')
        if ut.checkanswer(answer,quiz.question_content.get('answers'))!=True:
            messages.error(request, 'Wrong Answer, please try again')
            return HttpResponseRedirect(reverse('quiz:quiz',args=(user_id,question_title,)))
        quiz.ifpassed=True
        quiz.save()
        return HttpResponseRedirect(reverse('quiz:userface', args=(user_id,)))



