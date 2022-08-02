from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from simple_judge.models import Student, Question, Questiondict
from django.contrib.auth.decorators import login_required
import quiz.utils as ut
import markdown
import datetime
# Create your views here.


@login_required(login_url='/repolab/signin',redirect_field_name='/content/index')
def userface(request):
    return render(request, 'quiz/problems.html')

@login_required(login_url='/repolab/signin',redirect_field_name='/content/assignment')
def assignment(request):
    student=Student.objects.get(student_netid=request.user.username)
    context={}

    ## All the assignments that are between the pub_date and due_date
    question_due_dict= student.question_due_dict

    due_date = [i[1] for i in question_due_dict.items()]

    # filter the quiz that is not open, and show the quiz whose state is either open or passed  // open for 1, and passed for -1
    due_dict = ut.checktime(question_due_dict)
    # array=list(zip (a,b,d,e))

    progress_array, passed_array = ut.get_progress(student.question_set.all(),len(due_dict))

    set=[101,201,301,401,501,601,701]
    context['array']=list(zip( due_dict.keys(), due_dict.values(), progress_array, set,due_date , passed_array))
    return render(request,'quiz/assignment.html',context)

@login_required(login_url='/repolab/signin',redirect_field_name='/content/account')
def account(request):
    student=Student.objects.get(student_netid=request.user.username)
    context={}
    context['user'] = request.user
    context['student']=student

    return render(request, 'quiz/account.html', context)

@login_required(login_url='/repolab/signin')
def check(request, question_id):
    student_current=Student.objects.get(student_name=request.user.username)
    quiz=student_current.question_set.get(question_id=question_id)
    if request.method=='POST':
        question_dict=Questiondict.objects.get(question_id=question_id)
        answer=ut.getanswer(request,len(question_dict.question_content.get('answers')),question_dict.question_type)
        quiz.logx+='#'.join(answer)+'@'+str(datetime.datetime.utcnow())[:19]+'$'
        quiz.save()
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
        return HttpResponseRedirect(reverse('quiz:quiz_new', args=(question_id, )))
    return HttpResponse('You are not allowed to see the page now')

@login_required(login_url='/repolab/signin',redirect_field_name='/content/assignment')
def quiz_new(request,question_id):
    
    student_current=Student.objects.get(student_name=request.user.username)
    question_dict=Questiondict.objects.get(question_id=question_id)
    question_week=question_dict.question_week
    q= student_current.question_set.get(question_id=question_id)
    quiz_description=question_dict.question_content.get('description')
    mult=True
    context={}

    time_array = student_current.question_due_dict.get("week"+str(question_week))
    time_start = datetime.datetime.strptime(time_array[0],'%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    time_end = datetime.datetime.strptime(time_array[1],'%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    if time_now > time_end:
        context['overdue']=True
    elif time_now >= time_start:
        pass
    else:
        return HttpResponse("The question is not open yet")

    if question_dict.question_type=='blank' or question_dict.question_type=='code':
        answers=question_dict.question_content.get('answers')
        mult=False
    else:
        answers=ut.mult_answer_convert(question_dict.question_content.get('answers'))

    # Find latest history
    if q.logx!="":
        answer_string_and_time = q.logx[q.logx.rfind('$',0,q.logx.rfind('$')-1)+1:]
        answer_sets  = answer_string_and_time[:answer_string_and_time.find('@')].split('#')
        context['recent_answer']=answer_sets
        if mult:
            context['recent_answer']=" ".join(answer_sets)
        recent=True

    question_sets_temp1=student_current.question_set.filter(question_id__gte=100*question_week , question_id__lte=100*(question_week+1)).order_by('question_id')

    text = markdown.markdown(quiz_description,extensions=[
    'markdown.extensions.fenced_code',
    'markdown.extensions.extra',
    'markdown.extensions.toc'
    ])


    context['text']=text
    context['question_dict']=Questiondict.objects.get(question_id=question_id)
    context['quiz']=q
    context['user_id']=student_current.student_id
    context['mult']=mult
    context['answers']=answers
    context['section']=question_dict.question_content.get('section')
    context['question_id']=question_id
    context['length']=len(question_sets_temp1)
    context['question_sets']=question_sets_temp1
    context['passed']=len(question_sets_temp1.filter(ifpassed=True))
    context['failed']=len(question_sets_temp1.filter(submission_times=0))
    context['ids']=ut.findid(question_id,len(question_sets_temp1))
    return render(request, 'quiz/quiz.html', context)

