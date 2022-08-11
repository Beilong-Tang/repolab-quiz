from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
#from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from simple_judge.models import Student, Question, Questiondict
from django.contrib.auth.decorators import login_required
import quiz.utils as ut
import markdown
import datetime
from utils.settings import question_due_dict
from django.db.models import Q
# Create your views here.

def record_online_time(minute = 30):
    tim = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=0))) #UTC Time
    return tim, tim+datetime.timedelta(minutes=minute)


@login_required(login_url='/signin',redirect_field_name='/cs201/index')
def userface(request):
    student = Student.objects.get(student_netid = request.user.username)
    student.online_time, student.offline_time  = record_online_time()     
    student.save() 
    context={}
    context['session']=request.session.get('username')
    return render(request, 'quiz/problems.html',context)

@login_required(login_url='/signin')
def assignment(request):
    
    student=Student.objects.get(student_netid=request.user.username)
    student.online_time, student.offline_time  = record_online_time()     
    student.save() 
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

@login_required(login_url='/signin')
def account(request):
    student=Student.objects.get(student_netid=request.user.username)
    student.online_time, student.offline_time  = record_online_time()     
    student.save() 
    context={}
    context['user'] = request.user
    context['student']=student
    context['admin']=Student.objects.get(student_netid=request.user.username).level>0
    return render(request, 'quiz/account.html', context)

@login_required(login_url='/signin')
def check(request, question_id):
    student_current=Student.objects.get(student_netid=request.user.username)
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

@login_required(login_url='/signin',redirect_field_name='/content/assignment')
def quiz_new(request,question_id):
    
    student_current=Student.objects.get(student_netid=request.user.username)
    student_current.online_time, student_current.offline_time  = record_online_time()     
    student_current.save() 
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


    question_sets_temp1=student_current.question_set.filter(question_id__gte=100*question_week , question_id__lte=100*(question_week+1)).order_by('question_id')

    text = markdown.markdown(quiz_description,extensions=[
    'markdown.extensions.fenced_code',
    'markdown.extensions.extra',
    'markdown.extensions.toc'
    ])


    context['text']=text
    context['question_dict']=Questiondict.objects.get(question_id=question_id)
    context['quiz']=q
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


## Admin Page
@login_required(login_url='/signin')
def admin(request):
    #if request.user.username !='admin':
    if Student.objects.get(student_netid=request.user.username).level<1:
        return HttpResponse("You do not have the level to see this page, so you cannot see the page")
    


    tim = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=0))) # UTC Time
    online_people_array = Student.objects.filter(offline_time__gte=tim).filter(level=0)
    context={}
    #context['online']=online_people_array
    context['online_number']=online_people_array.count()


    return render(request, 'quiz/admin.html',context)

@login_required(login_url='/signin')
def admin_assignment(request):
    if Student.objects.get(student_netid=request.user.username).level<1:
        return HttpResponse("You do not have the level to see this page, so you cannot see the page")
    
    context={}

    # context['quiz_due_dict']=question_due_dict
    #                                   i                            j
    # context['array']=list(zip(question_due_dict.keys(), question_due_dict.values()))

    # Finished people number
    s_array = Student.objects.filter(level=0)
    context['student_number'] = s_array.count()
    array_pass_num =[]
    array_almost_pass_num =[]
    array_passed_rate_percentage=[]
    array_submit_times=[]


    for i in range(1,8):
        student_pass_num = 0
        student_almost_pass_num = 0
        pass_question = 0
        pass_and_fail = 0
        submit_times = 0

        for s in Student.objects.filter(level=0):

            question_array = s.question_set.filter(question_id__gte=100*i , question_id__lte=100*(i+1))
            pass_and_fail_array =  question_array.filter( Q(ifpassed=True) | Q(submission_times=0))
            total_num = question_array.count()
            almost_pass_num = int(total_num * 0.8)
            pass_num = s.question_set.filter(question_id__gte=100*i , question_id__lte=100*(i+1)).filter(ifpassed=True).count()
            if pass_num >= almost_pass_num:
                student_almost_pass_num+=1
                if pass_num == total_num:
                    student_pass_num+=1

            pass_question += question_array.filter( ifpassed=True).count()
            pass_and_fail += pass_and_fail_array.count()

            for q in pass_and_fail_array:
                submit_times += 5 - q.submission_times
        
        
        array_pass_num.append(student_pass_num)
        array_almost_pass_num.append(student_almost_pass_num)
        if pass_and_fail==0:
            array_passed_rate_percentage.append(0)
            array_submit_times.append(0)
        else:
            array_passed_rate_percentage.append(round(pass_question/pass_and_fail,2))
            array_submit_times.append( round(submit_times/pass_and_fail,2) )
    
    #context['pass']=array_pass_num
    #context['almost']=array_almost_pass_num
        

    #                                   i                            j                        m  ,         k                 n                      ,   q
    context['array']=list(zip(question_due_dict.keys(), question_due_dict.values(),array_pass_num,array_almost_pass_num,array_passed_rate_percentage,array_submit_times))


    return render(request, 'quiz/admin_assignment.html',context)
    


@login_required(login_url='/signin')
# need to know the admin id
def admin_quiz(request,week):
    if Student.objects.get(student_netid=request.user.username).level<1:
        return HttpResponse("You do not have the level to see this page, so you cannot see the page")
    week_id = int(week[4:])
    q = Question.objects.filter(question_id__gte=100*week_id , question_id__lte=100*(week_id+1))
    q = q.order_by('submission_times')
    context={}
    context['q']=q

    array={}
    array_submit_times = {}

    for q in Questiondict.objects.filter(question_week=week_id):
        fail_num = Question.objects.filter(question_id=q.question_id).filter(submission_times=0).filter(~Q(id=12)).count()
        array[q.question_id]=fail_num
        questions = Question.objects.filter(question_id=q.question_id).filter(~Q(Q(submission_times=5)&Q(ifpassed=False)))
        questions_after = [q for q in questions if Student.objects.get(id=q.student_id).level==0]
        if len(questions_after)==0:
            continue
        num = 0
        for q in questions_after:
            num+=q.submission_times
        num = round((5 *len(questions_after)-num)/len(questions_after),2)
        array_submit_times[q.question_id]=num


    dic = {i:j for i, j in array.items() if j!=0 }
    
    sorted_dict = dict(sorted(dic.items(),key=lambda x:x[1],reverse=True))
    submit_sorted_dict = dict(sorted({i:j for i, j in array_submit_times.items() if j!=0 }.items(),key=lambda x:x[1],reverse=True))

    context['dict']=sorted_dict
    context['submit_dict']=submit_sorted_dict





    return render(request, 'quiz/admin_quiz.html',context)

    
