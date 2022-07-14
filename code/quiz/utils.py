# Put the function Here
from django.contrib.auth.models import User
from simple_judge.models import Question, Questiondict
from django.http import HttpResponse
import re

## Check Answer for Fill in the blank questions
def checkanswer(input,question_title,question_type):
    if question_type=='blank':
        return checkanswer_blank(input,Questiondict.objects.get(question_title=question_title).question_content.get('answers'))
    if question_type=='mult':
        return checkanswer_mult(input,Questiondict.objects.get(question_title=question_title).question_content.get('answers'))
    



def checkanswer_blank(input, answer_sets):
    input_sets=list (filter (lambda x : x!='',input.split(' ')))
    if len(input_sets)!=len(answer_sets):
        return False
    for i in range(0,len(input_sets)):
        if input_sets[i]!=answer_sets[i]:
            return False
    return True
## Check Answer for multi choice questions
def checkanswer_mult(input,answer_sets):    
    input_sets=list (filter (lambda x : x!='',input.split(' ')))
    answer_arrays=[]
    for i in range(0,len(answer_sets)):
        if answer_sets[i]=='True':
            answer_arrays.append(i+97)
    print(answer_arrays)
    try:
        input_answer=[ ord(char.lower()) for char in input_sets]
    except:
        return False
    return sorted(input_answer)==sorted(answer_arrays)

def checkuser(username,user_id):
    user_web = User.objects.get(pk=user_id)
    if (username!=user_web.username):
        return HttpResponse("You are not allowed to See the Page") 
    

def checkquestion(question_title, student):
    for i in student.question_set.all():
        if student.question_set.get(question_title=i).question_title==question_title:
            return True
    return False

def replace_blanks(question_description):
    # Replace '__(1)__' with '__\___(1)_____'
    r = '__[(][0-9]+[)]__'
    m=re.findall(r,question_description)
    for i in range(0,len(m)):
        question_description=question_description.replace('__('+(str)(i)+')__','_____('+(str)(i)+')\___')
    return question_description

