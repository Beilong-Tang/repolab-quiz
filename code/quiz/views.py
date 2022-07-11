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

from simple_judge.models import Student, Question, Questiondict
import quiz.utils as ut
import markdown
# Create your views here.

def checkuser(request,user_id):
    if request.user.username!=Student.objects.get(student_id=user_id).student_name:
        return False
    return True

def index(request):
    return HttpResponse("HelloThere!")

def student_user(user_id):

    student=Student.objects.get(student_id=user_id)
    return student


def userface(request,user_id):
    if checkuser(request , user_id) !=True:
       return HttpResponse("You are not allowed to See the Page") 
    student=Student.objects.get(student_name=request.user.username)
    context={}
    context['user_id']=user_id
    question_sets=student.question_set.filter(ifpassed=False)
    question_title=[question.question_title for question in question_sets]
    #context['question_sets']=student.question_set.filter(ifpassed=False)
    context['question_sets']=[Questiondict.objects.get(question_title=question.question_title) for question in question_sets]
    #quiz_level_sets

    return render(request, 'quiz/problems.html', context)
'''
def quiz(request,user_id,question_title):
    if checkuser(request,user_id)!=True:
        return HttpResponse("You are not allowed to See the Page")
    student_current=student_user(user_id)
    #return HttpResponse(question_title)  
    quiz=student_current.question_set.get(question_title=question_title)

    context={}
    context['user_id']=user_id
    context['question_title']=question_title
    #quiz_description=quiz.question_content.get('description').split('\n')
    quiz_description=Questiondict.objects.get(question_title=question_title).question_content.get('description')#.replace('\n','\n\n')#.split('\n')
    image_index=quiz_description.find('[image]')
    if image_index !=-1:
        quiz_description=quiz_description.replace('[image](','[image](/static/quiz')
    if '%s' in quiz_description:
        quiz_description=quiz_description.replace('%s','**Choices:**\n\n'+'\n\n'.join(Questiondict.objects.get(question_title=question_title).question_content.get('choices')))
    #quiz_description=x.convert("## Programming in Java \n```java\n System.out.println(1)\n```\n\n\nTo introduce you to developing Java programs, we break the process\ndown into three steps. To program in Java, you need to:\n\n- __(0)__ a program by typing it into a file named, say,\n  MyProgram.java.\n\n- __(1)__ it by typing __(2)__ MyProgram.java in a __(3)__\n  window.\n\n- __(4)__ (or run) it by typing java MyProgram in the __(5)__\n  window.\n\n\nExcerpt From\nComputer Science\nSedgewick, Robert,Wayne, Kevin\nThis material may be protected by copyright.")

    context['quiz_description']=quiz_description
    
    return HttpResponse(quiz_description)
    return render(request, 'quiz/quiz.html', context)
'''
def check(request, user_id, question_title):
    if checkuser(request,user_id)!=True:
        return HttpResponse("You are not allowed to See the Page")
    student_current=student_user(user_id)
    quiz=student_current.question_set.get(question_title=question_title)

    if request.method=='POST':
        answer=request.POST['answer'].split(' ')
        if ut.checkanswer(answer,Questiondict.objects.get(question_title=question_title).question_content.get('answers'))!=True:
            messages.error(request, 'Wrong Answer, please try again')
            return HttpResponseRedirect(reverse('quiz:quiz',args=(user_id,question_title,)))
        quiz.ifpassed=True
        quiz.save()
        return HttpResponseRedirect(reverse('quiz:userface', args=(user_id,)))

def quiz_new(request,week,question_title):
    if request.user.is_authenticated:
        student_current=Student.objects.get(student_name=request.user.username)
        if ut.checkquestion(question_title,student_current):
            context={}
            context['question_title']=question_title
            quiz_description=Questiondict.objects.get(question_title=question_title).question_content.get('description')#.replace('\n','\n\n')#.split('\n')
            if '%s' in quiz_description:
                quiz_description=quiz_description.replace('%s','**Choices:**\n\n'+'\n\n'.join(Questiondict.objects.get(question_title=question_title).question_content.get('choices')))
            image_index=quiz_description.find('[image]')
            if image_index !=-1:
                quiz_description=quiz_description.replace('[image](','[image](/static/quiz/images/')
            context['quiz_description']=quiz_description
            return render(request, 'quiz/quiz.html', context)
        else:

            return HttpResponse(request.user.username)
    else:
        context={}
        context['question_title']=question_title
        quiz_description=Questiondict.objects.get(question_title=question_title).question_content.get('description')#.replace('\n','\n\n')#.split('\n')
        if '%s' in quiz_description:
            quiz_description=quiz_description.replace('%s','**Choices:**\n\n'+'\n\n'.join(Questiondict.objects.get(question_title=question_title).question_content.get('choices')))
        context['quiz_description']=quiz_description
        return render(request, 'quiz/quiz.html', context)
