from django.shortcuts import render
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
)

from django.urls import reverse
from simple_judge.models import Student, Questiondict
from forum.models import Comment, Post


import datetime
from django.db.models import Q
import os
from repolab.settings import BASE_DIR

## This is online img path
savedir = os.path.join(BASE_DIR,'static/forum/images/')

## This is local img path
#savedir = os.path.join(BASE_DIR,'forum/static/forum/images/')
# Create your views here.

def record_online_time(minute = 30):
    tim = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=0))) #UTC Time
    return tim, tim+datetime.timedelta(minutes=minute)

def userface(request):
    return HttpResponse("Hello")

def forum(request,filt):
    context={}

    
    student = Student.objects.get(student_netid=request.user.username)
    student.online_time, student.offline_time  = record_online_time()     
    student.save()

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
    context['comment_seen']= [Comment.objects.get(id=comment_id).post_id for comment_id in comment_seen]
    return render(request, 'forum/forum.html',context)

def forum_post(request, id, roll,textroll,filt):
    
    roll = int(float(roll))
    context={}
    current_post = Post.objects.get(id=id)

    student = Student.objects.get(student_netid=request.user.username)
    
    student.online_time, student.offline_time  = record_online_time()     
    student.save()


    # post_seen is actually post unseen
    if student.forum_seen.find(str(id)+',')!=-1:
        student.forum_seen=student.forum_seen.replace(str(id)+',','')
        student.save()


    post_seen = list(map(int,(list(filter(lambda x: x!="", student.forum_seen.split(','))))))
    post_star = list(map(int,(list(filter(lambda x: x!="", student.forum_star.split(','))))))
    comment_seen = list(map(int,(list(filter(lambda x: x!="", student.comment_seen.split(','))))))
    message_seen = list(map(int,(list(filter(lambda x: x!="", student.messages.split(','))))))
    context['new_comment'] = comment_seen

    # delete the comment in commen seen 
    if(roll!=-1):
        for comment_id in comment_seen:
            if Comment.objects.get(id=comment_id) in Comment.objects.filter(post_id=id):
                student.comment_seen = student.comment_seen.replace(str(comment_id)+',','')

        for message_id in message_seen:
            if Comment.objects.get(id=message_id) in Comment.objects.filter(post_id=id):
                student.messages = student.messages.replace(str(message_id)+',','')
        
        student.save()

    comment_seen = list(map(int,(list(filter(lambda x: x!="", student.comment_seen.split(','))))))

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
    context['comment_seen']=[Comment.objects.get(id=comment_id).post_id for comment_id in comment_seen] # This is actually the post id 
    
    
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

        title  = request.POST['title']
        level= int(request.POST['level'])
        category = int(request.POST['category'])
        problem = int(request.POST['question_input'])
        question_id = (category+1)*100+problem
        author =  Student.objects.get(student_netid=request.user.username)
        author.online_time, author.offline_time  = record_online_time()     
        author.save()
        author_name = author.student_name
        author_netid = author.student_netid
        time_now = datetime.datetime.utcnow()+datetime.timedelta(hours=8)
        pub_date = time_now.astimezone(datetime.timezone(datetime.timedelta(hours=0))) #utc+8 now
        p = Post(text=text, title=title, author_name = author_name, pub_date=pub_date,level=level,category=category,author_netid=author_netid,question_id=question_id)
        p.save()

        if img_length !='0':
            #return HttpResponse(request.FILES.get('0img').name)
            for i in range(0,int(img_length)):
                img_title = str(i)+'img'
                ## imgfile
                img = request.FILES.get(img_title)
                ## savedir

                # student_netid + post_id + img.name
                # example : bt132_10_HelloWorld.jpg
                

                back = img.name[img.name.find('.'):]

                img_name = request.user.username +'_'+str(p.id)+'_'+datetime.datetime.strftime(time_now,'%Y-%m-%d-%H-%M-%S')+'_'+str(i)+'_'+back


                img_path = os.path.join(savedir, img_name)
                with open(img_path, 'wb') as fp:
                    for chunk in img.chunks():
                        fp.write(chunk)
                p.text=p.text+"\n\n"+"![image](/static/forum/images/"+img_name+")"
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
        s.online_time, s.offline_time  = record_online_time()     
        s.save()
        if s.forum_star.find(id+',')==-1:
            s.forum_star+=id+','
            s.save()
        else:
            s.forum_star=s.forum_star.replace(id+',','')
            s.save()


    return HttpResponseRedirect(reverse('forum:forum_post' ,args=(id,roll,0,filt,)) )


def save_comment(request, id, roll, textroll,filt):

    comment_text = request.POST['comment_text']
    reply=int(request.POST['comment_id'])
    author = Student.objects.get(student_netid=request.user.username)
    author.online_time, author.offline_time  = record_online_time()     
    author.save()
    author_name = author.student_name
    author_netid = author.student_netid
    pub_date = datetime.datetime.utcnow().astimezone(datetime.timezone(datetime.timedelta(hours=8))) #utc now

    post = Post.objects.get(id=id)
    comment = post.comment_set.create(text=comment_text, author_name=author_name, author_netid=author_netid, pub_date=pub_date,reply=reply)
    post.save()
    
    img_length = request.POST['img_length']

    if img_length != '0':
        
        for i in range(0,int(img_length)):
            img_title = str(i)+'img'

            img = request.FILES.get(img_title)
            ## savedir
            
            # student_netid + post_id +i + img.name
            # example : Alice_108_2022-08-13-19-27-55_1.png
            
            back = img.name[img.name.find('.'):]

            img_name = request.user.username +'_'+str(comment.id)+'_'+datetime.datetime.strftime(datetime.datetime.utcnow()+datetime.timedelta(hours=8),'%Y-%m-%d-%H-%M-%S')+'_'+str(i)+back


            img_path = os.path.join(savedir, img_name)
            with open(img_path, 'wb') as fp:
                for chunk in img.chunks():
                    fp.write(chunk)
            comment.text=comment.text+"\n\n"+"![image](/static/forum/images/"+img_name+")"
         
        comment.save()

    for student in Student.objects.all():
        if str(id)+',' not in student.forum_seen:
            student.comment_seen += str(comment.id)+','
            student.save()

    ## Think of who involved in the POST, need to send messages to them!
    comments = post.comment_set.all()

    ## This author is the author that we would need to send messages, so that it filters the author him/herself
    authors = []
    for comment in comments:
        if comment.author_netid not in authors and comment.author_netid != author_netid:
            authors.append(comment.author_netid)


    Poster = Student.objects.get(student_netid=post.author_netid)
    Commenters = [Student.objects.get(student_netid=author_netid) for author_netid in authors]

    Poster.messages+=str(comment.id)+','
    Poster.save()
    for commenter in Commenters:
        commenter.messages+=str(comment.id)+','
        commenter.save()

    return HttpResponseRedirect(reverse('forum:forum_post' ,args=(id,roll,textroll,filt,)))
