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
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('quiz:userface'))

    return render(request,'simple_judge/index.html')


def signin(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('quiz:userface'))

    if request.method == 'POST':
        username= request.POST['username']
        pass1= request.POST['pass1']
        
        user = authenticate(username=username,password=pass1)

        if user is not None:
            request.session['a']=11
            request.session.set_expiry(1209600)
            login(request, user)
            # return HttpResponseRedirect(reverse('quiz:userface', args=(Student.objects.get(student_name=request.user.username),)))
            return HttpResponseRedirect(reverse('quiz:userface'))
        
        else:
            context={}
            context['username']=username
            context['pass1']=pass1
            messages.error(request, 'Either your id or your password is not right, please try again.')
            return render(request,'simple_judge/signin.html',context)

    return render(request,'simple_judge/signin.html')



def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('simple_judge:index'))

def change_password(request):
    
    if request.method=='POST':
        raw_pass = request.POST['raw_pass']
        pass1 = request.POST['pass1']

        user = authenticate(username=request.user.username, password=raw_pass)

        if user is not None:
            u = User.objects.get(username=request.user.username)
            u.set_password(pass1)
            u.save()
            messages.success(request, "Your new password is set up, please re-login.")
            logout(request)
            return HttpResponseRedirect(reverse('simple_judge:signin'))

        else:
            context={}
            context['raw_pass']=raw_pass
            context['pass1']=pass1
            messages.error(request, "The current password is not right")
            return render(request, 'simple_judge/change_password.html',context)

    else:
        context={}
        user = User.objects.get(username=request.user.username)
        return render(request, 'simple_judge/change_password.html',context)

