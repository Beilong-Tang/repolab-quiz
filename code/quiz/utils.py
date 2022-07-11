# Put the function Here
from django.contrib.auth.models import User
from django.http import HttpResponse
## Check Answer for Multi-choice questions and Fill in the blank questions
def checkanswer(input_sets, answer_sets):
    if len(input_sets)!=len(answer_sets):
        return False
    for i in range(0,len(input_sets)):
        if input_sets[i]!=answer_sets[i]:
            return False
    return True

def checkuser(username,user_id):
    user_web = User.objects.get(pk=user_id)
    if (username!=user_web.username):
        return HttpResponse("You are not allowed to See the Page") 
    

def checkquestion(question_title, student):
    for i in student.question_set.all():
        if student.question_set.get(question_title=i).question_title==question_title:
            return True
    return False