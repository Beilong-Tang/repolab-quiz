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
from simple_judge.models import Student
# Create your views here.
def index(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('quiz:userface', args=(Student.objects.get(student_name=request.user.username).student_id,)))

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
            return HttpResponseRedirect(reverse('quiz:userface', args=(Student.objects.get(student_name=request.user.username).student_id,)))
        
        else:
            messages.error(request, 'Either your id or your password is not right, please try again.')
            return HttpResponseRedirect(reverse('simple_judge:signin'))

    return render(request,'simple_judge/signin.html')



def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('simple_judge:index'))

def signin_from_question(request,week,question_title):
    context={}
    context['week']=week
    context['question_title']=question_title
    if request.method == 'POST':
        username= request.POST['username']
        pass1= request.POST['pass1']

        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request, user)
            fname=user.first_name
            return HttpResponseRedirect(reverse('quiz:quiz_new', args=(week,question_title,)))
        
        else:
            messages.error(request, 'Bad Credentials')
            return HttpResponseRedirect(reverse('simple_judge:signin_from_question'))

    return render(request,'simple_judge/signin_q.html',context)


def change_password(request):
    context={}
    if request.method=='POST':
        raw_pass = request.POST['raw_pass']
        pass1 = request.POST['pass1']
        #pass2 = request.POST['pass2']
        
        user = authenticate(username=request.user.username, password=raw_pass)

        if user is not None:
            u = User.objects.get(username=request.user.username)
            u.set_password(pass1)
            u.save()
            messages.success(request, "Your new password is set up, please re-login.")
            logout(request)
            return HttpResponseRedirect(reverse('simple_judge:signin'))


        else:
            context['raw_pass']=raw_pass
            context['pass1']=pass1
            context['user_id']= Student.objects.get(student_netid=request.user.username).student_id
            messages.error(request, "The current password is not right")
            return render(request, 'simple_judge/change_password.html',context)



    else:
        user = User.objects.get(username=request.user.username)
        context['user_id']= Student.objects.get(student_netid=request.user.username).student_id
        return render(request, 'simple_judge/change_password.html',context)


    return HttpResponse(user.password)
    pass







