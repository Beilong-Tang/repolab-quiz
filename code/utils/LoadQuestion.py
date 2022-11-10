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

import json
import re

import yaml

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'repolab.settings')
# django.setup()

from .settings import quiz_dir
from .settings import quiz_necessary_elements
from .settings import quiz_non_necessary_elements

from .question_title import question_title_change 

from simple_judge.models import Question, Student, Questiondict

week=[100,200,300,400,500,600,700]

def MergePath(a,b):
    return a+'/'+b

def LoadQuestion_yaml(command_week:str) ->None:
    bank_path = os.path.join(os.path.dirname(os.getcwd()),'repolab-quiz','bank')
    content:list = yaml.load(open(os.path.join(bank_path,'Quiz.yml')), Loader=yaml.FullLoader)[command_week] # This part shall be changed 
    print(content)
    week = int(command_week[4])
    for index , quiz in enumerate(content):
        find = re.search('sec-(\d.\d)-(\w+).(\d+)',quiz).groups()
        # section = find[0] # '1.1' # quiz_type = find[1]  # 'quiz'# quiz_id = find[2] # 0
        print(find)
        if find[1]=='quiz':
            # fill in the blank question
            path = os.path.join(bank_path, 'princeton-book', 'chap0%s'% find[0][0] , 'sec-%s'%find[0], 'quiz-gen')
            json_name = list(filter(lambda x: x.startswith(find[1]+'.'+find[2]), os.listdir(path)))[0]
            json_file = os.path.join(path,json_name)
        elif find[1]=='mult':
            path = os.path.join(bank_path, 'mult', 'chap0%s'% find[0][0] , 'sec-%s'%find[0])
            json_name = list(filter(lambda x: x.startswith(find[1]+'.'+find[2]), os.listdir(path)))[0]
            json_file = os.path.join(path,json_name)
        elif find[1]=='code':
            path = os.path.join(bank_path, 'code', 'chap0%s'% find[0][0] , 'sec-%s'%find[0],'quiz-gen')
            json_name = list(filter(lambda x: x.startswith(find[1]+'.'+find[2]), os.listdir(path)))[0]
            json_file = os.path.join(path,json_name)
            

        json_content:dict = json.load(open(json_file))
        json_content['section']=find[0]
        
        question_id = week*100+index+1

        if (Questiondict.objects.filter(question_id=week*100+index+1).exists()):
            q = Questiondict.objects.get(question_id=question_id)
            ## Just Update the quiz 
            q.question_type = ModifyType(json_content['quiz_type'])
            q.question_title = FindTitle(json_content['quiz_type'],json_name)
            q.question_content=ModifyContent(json_content,json_content['quiz_type'],question_id)
            q.question_id=question_id
            q.question_level=int(json_content['level'])
            q.question_week=week
            q.save()
        else:
            q= Questiondict(question_type=ModifyType(json_content['quiz_type']),
                            question_title=FindTitle(json_content['quiz_type'],json_name),
                            question_content=ModifyContent(json_content,json_content['quiz_type'],question_id),
                            question_id=question_id,
                            question_level=int(json_content['level']),
                            question_week=week
                            )
            q.save()
    print("finished loading question from %s" % command_week)
    
    return
            
    pass




# DumpQuestion(week1)
def DumpQuestion(command_week):
    print("DumpQuestion " , command_week)
    if not os.path.exists('qbank'): os.system('mkdir qbank')
    for q in Questiondict.objects.filter(question_week = int(command_week[4])):
        a = {}
        a['question_type'] = q.question_type
        a['question_title'] = q.question_title
        a['question_content'] = q.question_content
        a['question_level'] = q.question_level
        a['question_id'] = q.question_id
        a['question_week' ] = q.question_week
        w = 'qbank/week' + str(a['question_week'])
        fname = 'qbank/week%s/%s.json'% (a['question_week'], a['question_id'])
        if not os.path.exists(w): os.system('mkdir '+w)
        open(fname, 'w').write(json.dumps(a,indent=2))
        pass
    pass

def LoadQuestion3_single(id):
    try: 
        id = int(id)
    except:
        print("Error, id not legal")
        return
    q = Questiondict.objects.get(question_id=id)
    week = id // 100
    with open('qbank/week%s/%s.json' % (str(week), str(id)),'r') as f:
        d = json.load(f)
    q.question_type= d['question_type']
    q.question_title=d['question_title']
    q.question_content=d['question_content']
            #        q.question_id=d['question_id']
    q.question_level=int(d['question_level'])
    q.question_week=int(d['question_week'])
    q.save()
    print('question%s loaded' % str(id))
    return




# LoadQuestion('week1')
def LoadQuestion2(command_week ,id):
    # load everything from the week
    id_all=[]
    for q in Questiondict.objects.filter(question_week = int(command_week[4])):
        id_all.append(q.question_id)
        pass
    w = 'qbank/'+ command_week
    question_array=list(filter(lambda x: x.endswith('.json'), os.listdir(w)))
    for i in question_array:
        f = w + '/' + i
#        print(f)
        d = json.loads(open(f,'r').read())
        
        if  d['question_id'] not in id_all:
            
            print('init: ', d['question_id'])
            q= Questiondict(question_type= d['question_type'],
                            question_title=d['question_title'],
                            question_content=d['question_content'],
                            question_id=d['question_id'],
                            question_level= int(d['question_level']),
                            question_week=d['question_week'],
                            )
            q.save()
        else:
            print('update: ', d['question_id'])
            q = Questiondict.objects.get(question_id= d['question_id'])
            ## Just Update the quiz 
            q.question_type= d['question_type']
            q.question_title=d['question_title']
            q.question_content=d['question_content']
            #        q.question_id=d['question_id']
            q.question_level=int(d['question_level'])
            q.question_week=int(d['question_week'])
            q.save()
            
def LoadQuestion(command_week):

    dir_now=os.getcwd()

    os.chdir(quiz_dir)

    os.system('python3 manage.py '+command_week)

    os.chdir(dir_now)
    
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
                                question_content=ModifyContent(json_content,json_content['quiz_type'],question_id),
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
                q.question_content=ModifyContent(json_content,json_content['quiz_type'],question_id)
                q.question_id=json_content['id']
                q.question_level=int(json_content['level'])
                q.question_week=FindWeek(question_id)
                q.save()


    print('finished')

    return specific_week_folder


def ModifyContent(json_content,quiz_type,question_id):

    if json_content['description'].find('[image]'):
        json_content['description']=json_content['description'].replace('[image](','[image](/static/quiz/images/')
    ###
    json_content['description']=replace_blanks(json_content['description'])

    if quiz_type=='mult' or quiz_type=='JQ_MultiChoice':
        #quiz_description=quiz_description.replace('%s','**Choices:**\n\n'+'\n\n'.join(question_dict.question_content.get('choices')))
        json_content['description']='### Problem'+str(question_id)[1:]+'\n'+json_content['description']
        json_content['description']=json_content['description'].replace('%s','**Choices:**\n\n'+'\n\n'.join(json_content['choices']))
    else:
        json_content['description']='### Problem'+str(question_id)[1:]+'\n'+json_content['description'].lstrip('\n')[json_content['description'].lstrip('\n').find('\n')+1:]

    return json_content

    pass

def ModifyType(quiz_type):
    if quiz_type=='JQ_Code':
        return 'code'
    elif quiz_type=='JQ_MultiChoice':
        return 'mult'
    elif quiz_type=='JQ_UnorderedBlank':
        return 'blank'
    raise Exception("Quiz Type Error")


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


def replace_blanks(question_description):
    # Replace '__(1)__' with '__\___(1)_____'
    r = '__[(][0-9]+[)]__'
    m=re.findall(r,question_description)
    for i in range(0,len(m)):
        question_description=question_description.replace('__('+(str)(i)+')__','_____('+(str)(i)+')\___')
    return question_description


def week_id_check(command,hw_dir):

    
    week_array = ['week1','week2','week3','week4','week5','week6','week7']

    if command not in week_array:
        assert "Please type in the correct command" and False
    
    week_quiz_array=list(filter(lambda x: x.endswith('.json'),os.listdir(hw_dir+'/'+command)))

    if len(week_quiz_array)!=24:
        print("Question number is not 24")

    for quiz in week_quiz_array:
        file=hw_dir+'/'+command+'/'+quiz
        quiz_id=int(quiz[:quiz.find('.')])
        file_raw=open(file,'r')
        json_content=json.load(file_raw)
        file_raw.close()
        json_content['id']=int(command[4:])*100+quiz_id
        # Check(command, json_content,quiz):
        json_content=Check(command=command, json_content=json_content,quiz=quiz)[0]

        with open(file,'w') as f:
             json.dump(json_content,f,indent=2)

def Check(command, json_content,quiz):
    error = False
    for key in quiz_necessary_elements:
        if key  not in json_content.keys():
            error = True
            print('Warning:'+command+' '+quiz+' '+key+ ' not found')
        else:
            if key =='author':
                if json_content[key]=="":
                    error = True
                    print('Warning:'+command+' '+quiz+' author not initialized') 
            elif key =='section':
                if json_content[key]=="":
                    error = True
                    print('Warning:'+command+' '+quiz+' section not initialized') 
                else:
                    try:
                        flo = float(json_content[key])
                    except:
                        error = True
                        print('Warning:'+command+' '+quiz+' section not in the right format.') 
            elif key == 'description':
                if json_content[key]=="":
                    error = True
                    print('Warning:'+command+' '+quiz+' description.') 
            elif key == 'level':
                if json_content[key]=="":
                    error = True
                    print('Warning:'+command+' '+quiz+' level not initialized.') 
            elif key == 'quiz_type':
                if json_content[key]=='JQ_UnorderedBlank':
                    json_content[key]='blank'
                elif json_content[key]=='JQ_MultiChoice':
                    json_content[key]='mult'
                elif json_content[key]=='JQ_Code':
                    json_content[key]='code'
    
    for key in quiz_non_necessary_elements:
        if key in json_content.keys():
            del json_content[key]
    
    if 'explains' in json_content.keys():
        if isinstance(json_content['explains'],list):
            json_content['explains']="None"
    else:
        json_content['explains']="None"
    return json_content, error


if __name__=='__main__':
    week_id_check('week1',quiz_dir)
