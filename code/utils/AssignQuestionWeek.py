# 1. Assign Students 
#python3 shell.py assign
# from simple_judge.models import Student, Question, Questiondict
# from 
# 
# chap 1 10 ge
# chap 2 10 
# chap 3 10 
# chap 4 10 
# chap 5 10 
import random
from simple_judge.models import Question, Student, Questiondict
'''
from simple_judge.models import Question, Student, Questiondict
from utils.AssignQuestionWeek import question_assign_fixed_per_week as qafpw
for s in Student.objects.all():
   for q in s.question_set.all():
            q.delete()
'''
def question_assign_fixed_per_week(num=10,chap=7):
    '''
    iteration=1
    # iteration through chapters
    while iteration <=chap:
        question_chap_array=[]
        question_chap_array_init=[]
        # find question belonging to each week
        for q in Questiondict.objects.all():
            if q.question_week==iteration:
                question_chap_array_init.append(q)
        # Shuffle
        for s in Student.objects.all():
            question_chap_array=[]
            random.shuffle(question_chap_array_init)
            for i in range(0,num):
                question_chap_array.append(question_chap_array_init[i])
            ## The quiz is selected in the question_chap_array
            for quiz in question_chap_array:
                s.question_set.create(question_title=quiz.question_title,ifpassed=False)
            s.save()
            #s.save()
        iteration+=1
    '''
    for s in Student.objects.all():
        iteration=1
        while iteration <=chap:
            question_chap_array=[]
            question_chap_array_init=[]
        # find question belonging to each week
            for q in Questiondict.objects.all():
                if q.question_week==iteration:
                    question_chap_array_init.append(q)
            random.shuffle(question_chap_array_init)
            for i in range(0,num):
                question_chap_array.append(question_chap_array_init[i])
            for quiz in question_chap_array:
                s.question_set.create(question_title=quiz.question_title,ifpassed=False)
            s.save()
            iteration+=1



def generate_random_questions():
    args=""
    args+=" while i <"

def execute(default=True):
    #if default==True:

    pass


if __name__=='__main__':
    execute(default=True)



