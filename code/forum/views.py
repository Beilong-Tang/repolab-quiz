from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from numpy import record
from simple_judge.models import Student, Question, Questiondict
from forum.models import Comment, Post
from django.contrib.auth.decorators import login_required
import quiz.utils as ut
import markdown
import datetime
from utils.settings import question_due_dict
from django.db.models import Q

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

def forum_post(request, id, roll):

    context={}
    current_post = Post.objects.get(id=id)

    student = Student.objects.get(student_netid=request.user.username)


    if student.forum_seen.find(str(id)+',')==-1:
        student.forum_seen+=str(id)+','
        student.save()
    
    post_seen = list(map(int,(list(filter(lambda x: x!="",student.forum_seen.split(','))))))
    post_star = list(map(int,(list(filter(lambda x:x!="", student.forum_star.split(','))))))

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


    return render(request, 'forum/forum_post.html', context)

def create_post(request):
    if request.method=="POST":
        title  = request.POST['title']
        text = request.POST['text']
        level= int(request.POST['level'])
        category = int(request.POST['category'])
        author =  Student.objects.get(student_netid=request.user.username)
        author_name = author.student_name
        author_netid = author.student_netid
        pub_date = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=0))) #utc now
        p = Post(text=text, title=title, author_name = author_name, pub_date=pub_date,level=level,category=category,author_netid=author_netid)
        p.save()
        return HttpResponseRedirect(reverse('forum:forum'))

        pass

    context={}
    context['post']=Post.objects.all().order_by('-pub_date')

    return render(request, 'forum/create_post.html', context)

    pass


def save_star(request):
    if request.method=='POST':
        star_id = request.POST['star_id']
        s = Student.objects.get(student_netid=request.user.username)
        # save
        if request.POST['save']=='1':
            if s.forum_star.find(star_id+',')==-1:
                s.forum_star+=star_id+','
                s.save()
        # delete
        else:
            if s.forum_star.find(star_id+',')!=-1:
                s.forum_star=s.forum_star.replace(star_id+',','')
                s.save()

    
    pass