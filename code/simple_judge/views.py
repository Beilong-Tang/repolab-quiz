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
from simple_judge.models import Student
# Create your views here.
def index(request):
    
    return render(request,'simple_judge/index.html')


def signup(request):

    if request.method== "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! shitttttttt")
            return HttpResponseRedirect(reverse('simple_judge:signup'))

        if User.objects.filter(email=email):
            messages.error(request, "Email Already Registered")
            return HttpResponseRedirect(reverse('simple_judge:signup'))
        
        if len(username)>10:
            messages.error(request, "username must be under 10 characters")
            return HttpResponseRedirect(reverse('simple_judge:signup'))
        
        if pass1 != pass2:
            messages.error (request, "Passwords didn't match!")
            return HttpResponseRedirect(reverse('simple_judge:signup'))

        if not username.isalnum():
            messages.error(request, "username must be alpha-numeric")
            return HttpResponseRedirect(reverse('simple_judge:signup'))


        myuser= User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name = lname
        myuser.save()
        messages.success (request, "Your account has been successfully created")

        return HttpResponseRedirect(reverse('simple_judge:index'))

    return render(request, 'simple_judge/signup.html')



def signin(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('quiz:userface', args=(Student.objects.get(student_name=request.user.username).student_id,)))

    if request.method == 'POST':
        username= request.POST['username']
        pass1= request.POST['pass1']

        user = authenticate(username=username,password=pass1)


        if user is not None:
            login(request, user)
            fname=user.first_name
            return HttpResponseRedirect(reverse('quiz:userface', args=(Student.objects.get(student_name=request.user.username).student_id,)))
        
        else:
            messages.error(request, 'Bad Credentials')
            return HttpResponseRedirect(reverse('simple_judge:signin'))

    return render(request,'simple_judge/signin.html')
    #return HttpResponseRedirect(reverse('quiz:userface', args=(request.user.pk,)))


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('simple_judge:index'))









