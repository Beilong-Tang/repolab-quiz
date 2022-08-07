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

savedir = os.path.join(BASE_DIR,'forum/static/forum/images/')
# Create your views here.

def userface(request):
    return HttpResponse("Hello")

def forum(request):
    context={}

    post=Post.objects.all().order_by('-pub_date')

    post_seen = list(map(int,list(filter(lambda x:x!='',Student.objects.get(student_netid=request.user.username).forum_seen.split(',')))))

    context['post_seen']=post_seen
    context['post']=post
    return render(request, 'forum/forum.html',context)

def forum_post(request, id, roll,textroll):

    context={}
    current_post = Post.objects.get(id=id)

    student = Student.objects.get(student_netid=request.user.username)


    if student.forum_seen.find(str(id)+',')==-1:
        student.forum_seen+=str(id)+','
        student.save()
    
    post_seen = list(map(int,(list(filter(lambda x: x!="", student.forum_seen.split(','))))))
    post_star = list(map(int,(list(filter(lambda x: x!="", student.forum_star.split(','))))))

    context['post']=Post.objects.all().order_by('-pub_date')

    context['current']=current_post
    context['text'] = markdown.markdown(current_post.text,extensions=[
    'markdown.extensions.fenced_code',
    'markdown.extensions.extra',
    'markdown.extensions.toc'
    ])
    context['post_seen']=post_seen
    context['roll'] = roll
    context['post_star']=post_star
    context['text_roll']=textroll

    return render(request, 'forum/forum_post.html', context)

def create_post(request):

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
        author =  Student.objects.get(student_netid=request.user.username)
        author_name = author.student_name
        author_netid = author.student_netid
        pub_date = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=0))) #utc now
        p = Post(text=text, title=title, author_name = author_name, pub_date=pub_date,level=level,category=category,author_netid=author_netid)
        p.save()
        return HttpResponseRedirect(reverse('forum:forum'))



    context={}
    context['post']=Post.objects.all().order_by('-pub_date')

    return render(request, 'forum/create_post.html', context)




def save_star(request,id,roll):

    if request.method=='POST':

        id=str(id)
        s = Student.objects.get(student_netid=request.user.username)
        if s.forum_star.find(id+',')==-1:
            s.forum_star+=id+','
            s.save()
        else:
            s.forum_star=s.forum_star.replace(id+',','')
            s.save()


    return HttpResponseRedirect(reverse('forum:forum_post' ,args=(id,roll,0,)) )


def save_comment(request, id, roll, textroll):


    # post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # text = models.TextField()
    # author_name = models.CharField(max_length=50)
    # author_netid = models.CharField(max_length=8)
    # pub_date = models.DateTimeField(default=datetime.datetime.strptime('2022-7-26 6:00','%Y-%m-%d %H:%M').astimezone(datetime

    comment_text = request.POST['comment_text']
    author = Student.objects.get(student_netid=request.user.username)
    author_name = author.student_name
    author_netid = author.student_netid
    pub_date = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=0))) #utc now

    post = Post.objects.get(id=id)
    post.comment_set.create(text=comment_text, author_name=author_name, author_netid=author_netid, pub_date=pub_date)
    post.save()
    
    return HttpResponseRedirect(reverse('forum:forum_post' ,args=(id,roll,textroll,)))

