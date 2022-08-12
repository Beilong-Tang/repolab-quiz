from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from simple_judge.models import Student, Question, Questiondict
from forum.models import Comment, Post
from django.contrib.auth.decorators import login_required
import quiz.utils as ut
import markdown
import datetime
from utils.settings import question_due_dict
from django.db.models import Q
import os
from repolab.settings import BASE_DIR
from repolab.settings import STATIC_ROOT

savedir = os.path.join(BASE_DIR,'static/forum/images/')
# Create your views here.

def userface(request):
    return HttpResponse("Hello")

def forum(request,filt):
    context={}

    
    student = Student.objects.get(student_netid=request.user.username)

    post_seen = list(map(int,list(filter(lambda x:x!='',student.forum_seen.split(',')))))
    comment_seen = list(map(int,(list(filter(lambda x: x!="", student.comment_seen.split(','))))))
    post_star = list(map(int,(list(filter(lambda x: x!="", student.forum_star.split(','))))))

    ## Second level filter 

    if filt == 'All':
        context['post']=Post.objects.all().order_by('-pub_date')
        
    elif filt =='Star':

        post = [Post.objects.get(id=star_id) for star_id in post_star]
        context['post']= post
    
    elif filt[0:2]=='We':
        week = int(filt[4:])
        context['post'] = Post.objects.filter(question_id__gte=week*100 ,question_id__lte=(week+1)*100).order_by('-pub_date')
        context['first']=filt
        context['problem'] = Questiondict.objects.filter(question_id__gte=week*100 ,question_id__lte=(week+1)*100).order_by('question_id')

    else :
        question_id = int(filt)
        week = int(filt[0:1])
        context['post'] = Post.objects.filter(question_id=question_id).order_by('-pub_date') 
        context['problem']=Questiondict.objects.filter(question_id__gte=100*week,question_id__lte=100*(week+1)).order_by('question_id')
        context['first']="Week"+str(week)
    

    context['post_star']=post_star
    context['post_seen']=post_seen

    context['filt']=filt
    context['comment_seen']=comment_seen
    return render(request, 'forum/forum.html',context)

def forum_post(request, id, roll,textroll,filt):

    context={}
    current_post = Post.objects.get(id=id)

    student = Student.objects.get(student_netid=request.user.username)
    #return HttpResponse(student.forum_seen)


    # post_seen is actually post unseen
    if student.forum_seen.find(str(id)+',')!=-1:
        student.forum_seen=student.forum_seen.replace(str(id)+',','')
        student.save()

    if student.comment_seen.find(str(id)+',')!=-1:
        student.comment_seen=student.comment_seen.replace(str(id)+',','')
        student.save()


    post_seen = list(map(int,(list(filter(lambda x: x!="", student.forum_seen.split(','))))))
    comment_seen = list(map(int,(list(filter(lambda x: x!="", student.comment_seen.split(','))))))
    post_star = list(map(int,(list(filter(lambda x: x!="", student.forum_star.split(','))))))

    if filt == 'All':
        context['post']=Post.objects.all().order_by('-pub_date')
        
    elif filt =='Star':

        post = [Post.objects.get(id=star_id) for star_id in post_star]
        context['post']= post
    
    elif filt[0:2]=='We':
        week = int(filt[4:])
        context['post'] = Post.objects.filter(question_id__gte=week*100 ,question_id__lte=(week+1)*100).order_by('-pub_date')
        context['first']=filt
        context['problem'] = Questiondict.objects.filter(question_id__gte=week*100 ,question_id__lte=(week+1)*100).order_by('question_id')

    else :
        question_id = int(filt)
        week = int(filt[0:1])
        context['post'] = Post.objects.filter(question_id=question_id).order_by('-pub_date') 
        context['problem']=Questiondict.objects.filter(question_id__gte=100*week,question_id__lte=100*(week+1)).order_by('question_id')
        context['first']="Week"+str(week)

    context['current']=current_post

    context['filt']=filt

    context['text']=current_post.text
    context['post_seen']=post_seen
    context['roll'] = roll
    context['post_star']=post_star
    context['text_roll']=textroll
    context['comment_seen']=comment_seen
    
    comment = current_post.comment_set.filter(reply=-1)
    context['comment_length']=comment.count()
    reply_array = current_post.comment_set.filter(~Q(reply=-1))
    reply=[]

    for c in comment:
        re = list(filter(lambda x: x.reply==c.id, reply_array))
        reply.append(re)
    
    context['comment_and_reply']=list(zip(comment,reply))
    

    return render(request, 'forum/forum_post.html', context)



def create_post(request,filt):
    
    if request.method=="POST":
        text = request.POST['text']
        img_length=request.POST['img_length']
        if img_length !='0':
            #return HttpResponse(request.FILES.get('0img').name)
            for i in range(0,int(img_length)):
                img_title = str(i)+'img'
                ## imgfile
                img = request.FILES.get(img_title)
                ## savedir
                img_name = img.name
                img_path = os.path.join(savedir, img_name)
                with open(img_path, 'wb') as fp:
                    for chunk in img.chunks():
                        fp.write(chunk)
                text=text+"\n\n"+"![image](/static/forum/images/"+img_name+")"
        
        title  = request.POST['title']
        level= int(request.POST['level'])
        category = int(request.POST['category'])
        problem = int(request.POST['question_input'])
        question_id = (category+1)*100+problem
        author =  Student.objects.get(student_netid=request.user.username)
        author_name = author.student_name
        author_netid = author.student_netid
        pub_date = (datetime.datetime.utcnow()+datetime.timedelta(hours=8)).astimezone(datetime.timezone(datetime.timedelta(hours=0))) #utc now
        p = Post(text=text, title=title, author_name = author_name, pub_date=pub_date,level=level,category=category,author_netid=author_netid,question_id=question_id)
        p.save()

        for student in Student.objects.all():
            student.forum_seen+=str(p.id)+','
            student.save()

        
        return HttpResponseRedirect(reverse('forum:forum', args=(filt,)))



    context={}
    context['post']=Post.objects.all().order_by('-pub_date')
    context['filt']=filt
    context['week_question_number'] = [ Questiondict.objects.filter(question_week =i ).count() for i in range(1,8)]

    return render(request, 'forum/create_post.html', context)




def save_star(request,id,roll,filt):

    if request.method=='POST':

        id=str(id)
        s = Student.objects.get(student_netid=request.user.username)
        if s.forum_star.find(id+',')==-1:
            s.forum_star+=id+','
            s.save()
        else:
            s.forum_star=s.forum_star.replace(id+',','')
            s.save()


    return HttpResponseRedirect(reverse('forum:forum_post' ,args=(id,roll,0,filt,)) )


def save_comment(request, id, roll, textroll,filt):


    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # text = models.TextField()
    # author_name = models.CharField(max_length=50)
    # author_netid = models.CharField(max_length=8)
    # pub_date = models.DateTimeField(default=datetime.datetime.strptime('2022-7-26 6:00','%Y-%m-%d %H:%M').astimezone(datetime

    comment_text = request.POST['comment_text']
    reply=int(request.POST['comment_id'])
    author = Student.objects.get(student_netid=request.user.username)
    author_name = author.student_name
    author_netid = author.student_netid
    pub_date = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=0))) #utc now

    post = Post.objects.get(id=id)
    post.comment_set.create(text=comment_text, author_name=author_name, author_netid=author_netid, pub_date=pub_date,reply=reply)
    post.save()
    
    for student in Student.objects.all():
        student.comment_seen += str(id)+','
        student.save()
    return HttpResponseRedirect(reverse('forum:forum_post' ,args=(id,roll,textroll,filt,)))

