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
# Create your views here.

def index(request):
    return HttpResponse("HelloThere!")

def userface(request,user_id):
    #user=authenticate(username='Alice', password='Alice')
    user_web = User.objects.get(pk=user_id)
    if (request.user.username!=user_web.username):
        return HttpResponse("You are not allowed to See the Page")
    student=Student.objects.get(student_id=user_id)
    

