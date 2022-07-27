'''
This file is to load the question from the current week folder from repolab-quiz. 
question_type
question_title
question_id
question_week
question_level
question_content

Dont run the file, since it will go wrong.
'''
import os
#from selectors import EpollSelector
import sys
import json
from utils.settings import quiz_dir
from utils.question_title import question_title_change 

#sys.path.append()
#from simple_judge.models import *
from simple_judge.models import Question, Student, Questiondict
#from simple_judge.models  import *

#print(os.listdir(quiz_dir))

week=[100,200,300,400,500,600,700]

def MergePath(a,b):
    return a+'/'+b

def ConvertWeek(command_week):
    week=int(command_week[4:])
    return week

# LoadQuestion('week1')
def LoadQuestion(command_week):
    week = ConvertWeek(command_week) # 1
    specific_week_folder = MergePath( quiz_dir , command_week ) 
    question_array=list(filter(lambda x: x.endswith('.json'), os.listdir(specific_week_folder)))

    id_all = []
    for q in Questiondict.objects.all():
        id_all.append(q.question_id)
    
    for question in question_array:
        question_path = MergePath( specific_week_folder, question )
        with open(question_path,'r') as f:
            json_content=json.load(f)
            question_id=json_content['id']
            # judge if the question_id alreadly exits
            if question_id not in id_all:
                q= Questiondict(question_type=json_content['quiz_type'],
                                question_title=FindTitle(json_content['quiz_type'],question),
                                question_content=json_content,
                                question_id=json_content['id'],
                                question_level=int(json_content['level']),
                                question_week=FindWeek(question_id)
                                )
                q.save()
            else:
                q = Questiondict.objects.get(question_id=question_id)
                ## Just Update the quiz 
                q.question_type = json_content['quiz_type']
                q.question_title = FindTitle(json_content['quiz_type'],question)
                q.question_content=json_content
                q.question_id=json_content['id']
                q.question_level=int(json_content['level'])
                q.question_week=FindWeek(question_id)
                q.save()


    print('finished')

    return specific_week_folder


def FindTitle(quiz_type,question_title_raw):
    print(question_title_raw)
    return question_title_change(question_title=question_title_raw,question_type=quiz_type)

def FindWeek(question_id):
    if question_id > 100 and question_id < 200:
        return 1
    elif question_id < 300:
        return 2
    elif question_id < 400:
        return 3
    elif question_id < 500:
        return 4
    elif question_id < 600:
        return 5
    elif question_id < 700:
        return 6
    elif question_id < 800:
        return 7




