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
import re
# Create your views here.

def checkuser(request,user_id):
    if request.user.username!=Student.objects.get(student_id=user_id).student_name:
        return False
    return True

def index(request):
    return HttpResponse("HelloThere!")
'''
def student_user(user_id):

    student=Student.objects.get(student_id=user_id)
    return student
'''

def userface(request,user_id):
    if checkuser(request , user_id) !=True:
       return HttpResponse("You are not allowed to See the Page") 
    student=Student.objects.get(student_name=request.user.username)
    context={}
    context['user_id']=user_id
    question_sets=student.question_set.all()#.filter(ifpassed=False)
    #context['question_sets']=student.question_set.filter(ifpassed=False)
    question_sets_after=[Questiondict.objects.get(question_title=question.question_title) for question in question_sets]
    #submission_times=[ i.submission_times for i in question_sets]
    #ifpass=[ i.ifpassed for i in question_sets]
    context['array']=list(zip(question_sets_after,question_sets))
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
def check(request, question_title):
    student_current=Student.objects.get(student_name=request.user.username)
    quiz=student_current.question_set.get(question_title=question_title)
    if request.method=='POST':
        answer=request.POST['answer']
        if ut.checkanswer(answer,question_title,Questiondict.objects.get(question_title=question_title).question_type)!=True:    
            messages.error(request, 'Wrong Answer, please try again')
            quiz.submission_times=quiz.submission_times-1
            quiz.save()
            return HttpResponseRedirect(reverse('quiz:quiz_new',args=(question_title,)))
        quiz.ifpassed=True
        quiz.save()
        return HttpResponseRedirect(reverse('quiz:quiz_new', args=(question_title,)))
    return HttpResponse('You are not allowed to see the page now')

def quiz_new(request,question_title):
    if request.user.is_authenticated:
        student_current=Student.objects.get(student_name=request.user.username)
        context={}
        context['user_id']=student_current.student_id
        if ut.checkquestion(question_title,student_current):
            context['question_title']=question_title
            quiz_description=Questiondict.objects.get(question_title=question_title).question_content.get('description')#.replace('\n','\n\n')#.split('\n')
            quiz_description=ut.replace_blanks(quiz_description)
            if '%s' in quiz_description:
                quiz_description=quiz_description.replace('%s','**Choices:**\n\n'+'\n\n'.join(Questiondict.objects.get(question_title=question_title).question_content.get('choices')))
            image_index=quiz_description.find('[image]')
            if image_index !=-1:
                quiz_description=quiz_description.replace('[image](','[image](/static/quiz/images/')
            context['quiz_description']=quiz_description
            context['submission_times']=student_current.question_set.get(question_title=question_title).submission_times
            context['week']=Questiondict.objects.get(question_title=question_title).question_week
            ## Input a array with the quiz title
            question_sets=student_current.question_set.all()
            question_sets_after=[Questiondict.objects.get(question_title=question.question_title) for question in question_sets] #[All the questions in Questiondict that is related to the question title]
            question_sets_temp1=list(filter(lambda x: x.question_week==context['week'], question_sets_after)) #[All the questions in Questiondict that belonggs the the certain week (Questiondict)]
            question_sets_temp2=[student_current.question_set.get(question_title=i.question_title) for i in question_sets_temp1] #[All the questions that belongs to the student (Question)]
            context['question_sets']=question_sets_temp2
            context['ifpassed']= student_current.question_set.get(question_title=question_title).ifpassed
            #context['ifpass']=student_current.question_set.get(question_title=question_title).ifpass
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

def week(request, user_id, week):
    if checkuser(request , user_id) !=True:
       return HttpResponse("You are not allowed to See the Page") 
    student=Student.objects.get(student_name=request.user.username)
    context={}
    context['user_id']=user_id
    question_sets=student.question_set.all() # ['All the questions in Alice ]
    #temp1= Questiondict.objects.filter()
    question_sets_after=[Questiondict.objects.get(question_title=question.question_title) for question in question_sets] #[All the questions in Questiondict that is related to the question title]
    question_sets_temp1=list(filter(lambda x: x.question_week==week, question_sets_after)) #[All the questions in Questiondict that belonggs the the certain week (Questiondict)]
    question_sets_temp2=[student.question_set.get(question_title=i.question_title) for i in question_sets_temp1] #[All the questions that belongs to the student (Question)]
    id=range(1,len(question_sets_temp1)+1)
    context['array']=list(zip( question_sets_temp1,question_sets_temp2,id))
    context['week']=week
    #quiz_level_sets

    return render(request, 'quiz/week.html', context)
