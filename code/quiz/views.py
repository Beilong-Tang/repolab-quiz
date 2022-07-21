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

# Create your views here.

week_now=2

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
    question_sets=student.question_set.all()#.filter(ifpassed=False)
    #return HttpResponse(question_sets)
    #context['question_sets']=student.question_set.filter(ifpassed=False)
    question_sets_after=[Questiondict.objects.get(question_title=question.question_title) for question in question_sets]
    #return HttpResponse(question_sets)
    # for question in question_sets:
    #     check=False
    #     n=0
    #     for i in Questiondict.objects.all():
    #         if n!=1 and i.question_title==question.question_title:
    #             n+=1
    #             check=True
    #             continue
    #         if n==1 and i.question_title==question.question_title:
    #             return HttpResponse(i.question_title+'    chongfu')
    #             check=False
    #             break
    #     if check==False:
    #         return HttpResponse(question)
    # return HttpResponse(1)
    #submission_times=[ i.submission_times for i in question_sets]
    #ifpass=[ i.ifpassed for i in question_sets]
    #context['array']=list(zip(question_sets_after,question_sets))
    #quiz_level_sets
    return render(request, 'quiz/problems.html', context)

def check(request, question_title):
    student_current=Student.objects.get(student_name=request.user.username)
    quiz=student_current.question_set.get(question_title=question_title)
    if request.method=='POST':
        question_dict=Questiondict.objects.get(question_title=question_title)
        answer=ut.getanswer(request,len(question_dict.question_content.get('answers')))
        if question_dict.question_week < week_now:
            return HttpResponseRedirect(reverse('quiz:quiz_new',args=(question_title,)))
        if ut.checkanswer(answer,question_title,question_dict.question_type,request.user.username)!=True:    
            messages.error(request, 'Wrong Answer!')
            if quiz.submission_times > 0 and quiz.ifpassed==False:
                quiz.submission_times=quiz.submission_times-1
                quiz.save()
            return HttpResponseRedirect(reverse('quiz:quiz_new',args=(question_title,)))
        messages.success(request, 'Correct Answer!')
        if quiz.ifpassed==True:
            return HttpResponseRedirect(reverse('quiz:quiz_new', args=(question_title,)))
        if quiz.submission_times > 0:
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
            question_dict=Questiondict.objects.get(question_title=question_title)
            question_week=question_dict.question_week
            context['overdue']=False
            if question_week <week_now:
                context['overdue']=True
            if question_dict.question_type=='blank' or question_dict.question_type=='code':
                context['answers']=question_dict.question_content.get('answers')
            context['question_title']=question_title
            ## The content here can be imporved
            quiz_description=question_dict.question_content.get('description')#.replace('\n','\n\n')#.split('\n')
            quiz_description=ut.replace_blanks(quiz_description)

            if question_dict.question_type=='mult':
                quiz_description=quiz_description.replace('%s','**Choices:**\n\n'+'\n\n'.join(question_dict.question_content.get('choices')))
            image_index=quiz_description.find('[image]')
            if image_index !=-1:
                quiz_description=quiz_description.replace('[image](','[image](/static/quiz/images/')
            ############################################
            context['quiz_description']=quiz_description
            q= student_current.question_set.get(question_title=question_title)
            context['submission_times']=q.submission_times
            context['week']=question_week
            ## Input an array with the quiz title
            question_sets_after=[Questiondict.objects.get(question_title=question.question_title) for question in student_current.question_set.all()] #[All the questions in Questiondict that is related to the question title]
            question_sets_temp1=list(filter(lambda x: x.question_week==context['week'], question_sets_after)) #[All the questions in Questiondict that belonggs the the certain week (Questiondict)]
            context['question_sets']=[student_current.question_set.get(question_title=i.question_title) for i in question_sets_temp1]
            context['ifpassed']= q.ifpassed
            set=[]
            for i in range(1,8):    
                q_w=list(filter(lambda x: student_current.question_set.get(question_title=x.question_title).ifpassed==False and student_current.question_set.get(question_title=x.question_title).submission_times>0, list(filter(lambda x: x.question_week==i,question_sets_after ))))[0]
                set.append(q_w)
            context['quiz_to']=set
            text = markdown.markdown(quiz_description,extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.extra',
            #'markdown.extensions.codehilite',
            'markdown.extensions.toc'
            # 'markdown.extensions.toc',
            ])
            context['text']=text
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
    question_sets_temp1=list(filter(lambda x: x.question_week==week,[Questiondict.objects.get(question_title=question.question_title) for question in question_sets])) #[All the questions in Questiondict that belonggs the the certain week (Questiondict)]
    question_sets_temp2=[student.question_set.get(question_title=i.question_title) for i in question_sets_temp1] #[All the questions that belongs to the student (Question)]
    id=range(1,len(question_sets_temp1)+1)
    context['array']=list(zip( question_sets_temp1,question_sets_temp2,id))
    context['week']=week
    #quiz_level_sets

    return render(request, 'quiz/week.html', context)

