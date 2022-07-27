from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from simple_judge.models import Student, Question, Questiondict
import quiz.utils as ut
import markdown
import datetime
# Create your views here.

week_now=1

def checkuser(request,user_id):
    if request.user.username!=Student.objects.get(student_id=user_id).student_name:
        return False
    return True

def index(request):
    return HttpResponse("Hello,There!")

def userface(request,user_id):
    if checkuser(request , user_id) !=True:
       return HttpResponse("You are not allowed to See the Page") 
    student=Student.objects.get(student_name=request.user.username)
    context={}
    context['user_id']=user_id
    return render(request, 'quiz/problems.html', context)

def check(request, question_id):
    student_current=Student.objects.get(student_name=request.user.username)
    quiz=student_current.question_set.get(question_id=question_id)
    if request.method=='POST':
        question_dict=Questiondict.objects.get(question_id=question_id)
        answer=ut.getanswer(request,len(question_dict.question_content.get('answers')),question_dict.question_type)
        if "" in answer or answer==[]:
            messages.warning(request,'You have unfinished blanks')
            return HttpResponseRedirect(reverse('quiz:quiz_new',args=(question_id,)))
        quiz.logx+='\\'.join(answer)+','+str(datetime.datetime.utcnow())[:19]+';'
        quiz.save()
        if question_dict.question_week < week_now:
            return HttpResponseRedirect(reverse('quiz:quiz_new',args=(question_id,)))
        if ut.checkanswer(answer,question_id,question_dict.question_type,request.user.username)!=True:    
            messages.error(request, 'Wrong Answer!')
            if quiz.submission_times > 0 and quiz.ifpassed==False:
                quiz.submission_times=quiz.submission_times-1
                quiz.save()
            return HttpResponseRedirect(reverse('quiz:quiz_new',args=(question_id,)))
        messages.success(request, 'Correct Answer!')
        if quiz.ifpassed==True:
            return HttpResponseRedirect(reverse('quiz:quiz_new', args=(question_id,)))
        if quiz.submission_times > 0:
            quiz.ifpassed=True
            quiz.save()
        return HttpResponseRedirect(reverse('quiz:quiz_new', args=(question_id,)))
    return HttpResponse('You are not allowed to see the page now')

def quiz_new(request,question_id):
    if request.user.is_authenticated:
        student_current=Student.objects.get(student_name=request.user.username)
        context={}
        context['user_id']=student_current.student_id
        if True:
            question_dict=Questiondict.objects.get(question_id=question_id)
            question_week=question_dict.question_week

            context['overdue']=False
            if question_week <week_now:
                context['overdue']=True
            if question_dict.question_type=='blank' or question_dict.question_type=='code':
                context['answers']=question_dict.question_content.get('answers')

            context['section']=question_dict.question_content.get('section')
            context['question_title']=question_dict.question_title
            context['question_id']=question_id
            quiz_description=question_dict.question_content.get('description')
            context['quiz_description']=quiz_description
            q= student_current.question_set.get(question_id=question_id)
            context['submission_times']=q.submission_times
            context['week']=question_week
            #question_sets_after=[Questiondict.objects.get(question_id=question.question_id) for question in student_current.question_set.all()] #[All the questions in Questiondict that is related to the question title]
            #question_sets_temp1=list(filter(lambda x: x.question_week==context['week'], question_sets_after)) #[All the questions in Questiondict that belonggs the the certain week (Questiondict)]
            question_sets_temp1=student_current.question_set.filter(question_id__gte=100*question_week , question_id__lte=100*(question_week+1)).order_by('question_id')
            #question_sets_after=[Questiondict.objects.get(question_id=question.question_id) for question in question_sets_temp1]
            context['question_sets']=question_sets_temp1
            context['ids']=ut.findid(question_id,len(question_sets_temp1))
            context['ifpassed']= q.ifpassed
            set=[101,201,301,401,501,101,701]
            context['quiz_to']=set
            text = markdown.markdown(quiz_description,extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.extra',
            'markdown.extensions.toc'
            ])
            context['text']=text
            return render(request, 'quiz/quiz.html', context)

    else:
        return HttpResponse('Please log in to see the page')

def week(request, user_id, week):
    if checkuser(request , user_id) !=True:
       return HttpResponse("You are not allowed to See the Page") 
    student=Student.objects.get(student_name=request.user.username)
    context={}
    context['user_id']=user_id
    question_sets=student.question_set.filter(question_id__gte=100*week , question_id__lte=100*(week+1)).order_by('question_id')
    question_dict_sets=[Questiondict.objects.get(question_id=question.question_id) for question in question_sets]
    context['array']=list(zip(question_sets,question_dict_sets))
    context['week']=week
    return render(request, 'quiz/week.html', context)

