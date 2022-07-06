import sys, os,subprocess,json
from utils.AssignWeek import assign_week_main as week
from utils.AssignQuestionWeek import execute
# Revise the Quiz director as where the quiz is at 

## Change the home_dir at here 
home_dir='/mnt/c/Users/Beilong Tang/Desktop/Main/CODE/DJANGO_new/repolab-quiz/bank'

########################################
instruction=""
quiz_set=""
importing='from simple_judge.models import Questiondict\nimport json\n'

# All the instructions are in the String 
# Questiondict(question_type='blank', question_title='test5', question_content={'description':1}).save()#
# 1. find question type
# question_title : princetonbook_chap01_sec-1.1_quiz.0.Programming.in.java
# 2. find question_content, which is a 

def generate_input_file_blank():

    args=importing
    args+=delete_blank()
    chap_dir=home_dir+'/'+'princeton-book'
    chapters=list(filter(lambda x: x.find('.')==-1 ,os.listdir(chap_dir)))
    chapters=list(filter(lambda x: x!='chap01',chapters))
    chapter_paths=[chap_dir+'/'+chapter for chapter in chapters]
    # Quiz_path is the quiz we want to do 
    #quiz_paths=[]
    #quiz_title=[]
    quiz_dict={}
    for i in chapter_paths:
        sections=list(filter(lambda x: os.path.isdir(i+'/'+x)==True, os.listdir(i)))
        for section in sections:
            section_path=i + '/' + section
            if 'quiz-gen' in os.listdir(section_path):
                quiz_file_path=section_path+'/quiz-gen'
                quiz_files=os.listdir(quiz_file_path)
                for quiz in quiz_files:
                    quiz_path=quiz_file_path+'/'+quiz
                    #quiz_paths.append(quiz_path)
                    quiz_title=quiz_path[quiz_path.find('princeton-book')+15:].replace('quiz-gen/','').replace('/','_').replace('json','blank')
                    #print(quiz_title)
                    quiz_dict[quiz_title]=quiz_path
                    args+="Questiondict(question_type='blank',question_title= '"+quiz_title+"',question_content={'description':1}).save()\n"
    # Change the question dict
    for i,j in quiz_dict.items():
        args+="q=Questiondict.objects.get(question_title='"+i+"')\n"
        args+="q.question_content=json.load(open('"+j+"','r'))\n"
        args+='q.save()\n'
    for i, j in quiz_dict.items():
        args+="q=Questiondict.objects.get(question_title='"+i+"')\n"
        args+="q.question_level=int('0' if q.question_content.get('level')==' ' or q.question_content.get('level')==''  else q.question_content.get('level'))\n"
        args+="q.save()\n"
    open('input.txt','w').write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

def generate_input_mult_choice():
    args=importing
    args+=delete_mult()
    chap_dir=home_dir+'/'+'mult'
    chapters=list(filter(lambda x: x.find('.')==-1 ,os.listdir(chap_dir)))
    #chapters=list(filter(lambda x: x!='chap01',chapters))
    chapter_paths=[chap_dir+'/'+chapter for chapter in chapters]
    # Quiz_path is the quiz we want to do 
    #quiz_paths=[]
    #quiz_title=[]
    quiz_dict={}
    for i in chapter_paths:
        sections=list(filter(lambda x: os.path.isdir(i+'/'+x)==True, os.listdir(i)))
        for section in sections:
            section_path=i + '/' + section
            if True:
                quiz_file_path=section_path
                quiz_files=os.listdir(quiz_file_path)
                #print(quiz_files)
                for quiz in quiz_files:
                    #print(quiz)
                    if quiz.find('.json')==-1:
                        continue
                    quiz_path=quiz_file_path+'/'+quiz 
                    quiz_title=quiz_path[quiz_path.find('mult')+5:].replace('/','_').replace('json','mult')
                    quiz_dict[quiz_title]=quiz_path
                    print(quiz_title)
                    args+="Questiondict(question_type='mult',question_title= '"+quiz_title+"',question_content={'description':1}).save()\n"
    # Change the question dict
    for i,j in quiz_dict.items():
        args+="q=Questiondict.objects.get(question_title='"+i+"')\n"
        args+="q.question_content=json.load(open('"+j+"','r'))\n"
        args+='q.save()\n'
    for i, j in quiz_dict.items():
        args+="q=Questiondict.objects.get(question_title='"+i+"')\n"
        args+="q.question_level=int('0' if q.question_content.get('level')==' ' or q.question_content.get('level')==''  else q.question_content.get('level'))\n"
        args+="q.save()\n"
    open('input.txt','w').write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)


def generate_input_code_question():

    args=importing
    args+=delete_code()
    chap_dir=home_dir+'/'+'code'
    chapters=list(filter(lambda x: x.find('.')==-1 ,os.listdir(chap_dir)))
    #chapters=list(filter(lambda x: x!='chap01',chapters))
    chapter_paths=[chap_dir+'/'+chapter for chapter in chapters]
    # Quiz_path is the quiz we want to do 
    #quiz_paths=[]
    #quiz_title=[]
    quiz_dict={}
    for i in chapter_paths:
        sections=list(filter(lambda x: os.path.isdir(i+'/'+x)==True, os.listdir(i)))
        for section in sections:
            section_path=i + '/' + section
            if 'quiz-gen' in os.listdir(section_path):
                quiz_file_path=section_path+'/quiz-gen'
                quiz_files=os.listdir(quiz_file_path)
                for quiz in quiz_files:
                    quiz_path=quiz_file_path+'/'+quiz
                    #quiz_paths.append(quiz_path)
                    quiz_title=quiz_path[quiz_path.find('code')+5:].replace('quiz-gen/','').replace('/','_').replace('json','code')
                    print(quiz_title)
                    quiz_dict[quiz_title]=quiz_path
                    args+="Questiondict(question_type='code',question_title= '"+quiz_title+"',question_content={'description':1}).save()\n"
    # Change the question dict
    for i,j in quiz_dict.items():
        args+="q=Questiondict.objects.get(question_title='"+i+"')\n"
        args+="q.question_content=json.load(open('"+j+"','r'))\n"
        args+='q.save()\n'
    for i, j in quiz_dict.items():
        args+="q=Questiondict.objects.get(question_title='"+i+"')\n"
        args+="q.question_level=int('0' if q.question_content.get('level')==' ' or q.question_content.get('level')==''  else q.question_content.get('level'))\n"
        args+="q.save()\n"
    open('input.txt','w').write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

def delete_code():
    return "for q in Questiondict.objects.all():\n    if q.question_type=='code':\n        q.delete()\n"

def delete_blank():
    return "for q in Questiondict.objects.all():\n    if q.question_type=='blank':\n        q.delete()\n"

def delete_mult():
    return "for q in Questiondict.objects.all():\n    if q.question_type=='mult':\n        q.delete()\n"


def input_and_execute(args):
    open('input.txt','w').write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

def execute():
    if sys.argv[1]=='blank':
        generate_input_file_blank()
        return
    if sys.argv[1]=='mult':
        generate_input_mult_choice()
        return
    if sys.argv[1]=='code':
        generate_input_code_question()
        return
    if sys.argv[1]=='week':
        if len(sys.argv)<3:
            input_and_execute(week(default=True))
            return
        input_and_execute(week(default=False,week=(int)(sys.argv[2]), chap=(int)(sys.argv[3]), section=sys.argv[4]))
        return
    #if sys.argv[1]=='assign':
      #  if len(sys.argv)<3:
      #  assign(default)
def input_instruction():
    args="from simple_judge.models import *\n"
    pass



if __name__=='__main__':
    execute()



    #open('input.txt','w').write(x)
    #ain=open('input.txt','r')
    ## This will run the process of storing the data
    #p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)
    #os.system(args)