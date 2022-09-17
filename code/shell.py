import sys, os,subprocess,json
#from utils.AssignWeek import assign_week_main as week
import utils as ut
#from utils.AssignQuestionWeek import execute
# Revise the Quiz director as where the quiz is at 

## Change the home_dir at here 
home_dir='/mnt/c/Users/Beilong Tang/Desktop/Main/CODE/DJANGO_new/repolab-quiz/bank'
home_dir='/mnt/c/Users/Beilong Tang/Desktop/Main/CODE/DJANGO_new/repolab-quiz/bank'
ldir = os.path.dirname(os.path.abspath(__file__))
home_dir='%s/../../repolab-quiz/bank'% ldir
########################################
instruction=""
quiz_set=""
importing='from simple_judge.models import Questiondict\nimport json\n'

first_command = ['week1','week2','week3','week4','week5','week6','week7']


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


def LoadQuestion(command, version =1):

    args=""
    args+="from simple_judge.models import Questiondict\n"
    if version == 1 :
        args+="from utils.LoadQuestion import LoadQuestion as f\n"
    elif version == 2:
        args+="from utils.LoadQuestion import LoadQuestion2 as f\n"
    else :
        args+="from utils.LoadQuestion import LoadQuestion3_single as f\n"

    args+="f('"+command+"')"

    with open ('input.txt','w') as f:
        f.write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)


    '''
    from simple_judge.models import Questiondict
    from utils import LoadQuestion.LoadQuestion as f
    f()
    '''
    pass
def DumpQuestion(command):
    
    args=""
    args+="from simple_judge.models import Questiondict\n"
    args+="from utils.LoadQuestion import DumpQuestion as f\n"
    args+="f('"+command+"')"
    
    with open ('input.txt','w') as f:
        f.write(args)
        ain=open('input.txt','r')
        p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)
        
        
        '''
        from simple_judge.models import Questiondict
        from utils import LoadQuestion.LoadQuestion as f
        f()
        '''

## This will assign question for all students
def AssignQuestion(student_netid=""):
    args=""
    args+="from simple_judge.models import Questiondict\n"
    args+="from utils.AssginQuestion import AssignQuestion as f\n"
    args+="f( '"+student_netid+"' )"

    with open ('input.txt','w') as f:
        f.write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)


def CreateUser(net_id, student_name,level):
    args = ""
    args+= "from simple_judge.models import Student\n"
    args+= "from django.contrib.auth.models import User\n"
    args+= "from utils.User import create_user as f\n"
    args+="f('"+net_id+"', '"+student_name+"' ,"+str(level)+")"
    with open ('input.txt','w') as f:
        f.write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

    pass

def ImportUser():
    args = ""
    args+= "from simple_judge.models import Student\n"
    args+= "from django.contrib.auth.models import User\n"
    args+= "from utils.User import importing_user as f\n"
    args+="from utils.settings import user_raw_path as user_raw_file\n"
    args+="f()"
    with open ('input.txt','w') as f:
        f.write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

def change_password_yaml():
    a = input('Warning: this function will reset all users\' passowrd to its raw status [y/n]')
    if a!='y':
        print('cancelled')
        return
    args = ""
    args+= "from simple_judge.models import Student\n"
    args+= "from django.contrib.auth.models import User\n"
    args+= "from utils.User import change_passowrd_yaml as f\n"
    args+="f()"
    with open ('input.txt','w') as f:
        f.write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

def change_passowrd(netid,new_password):
    a = input('Are u sure you want to change a password for a user? [y/n]')
    if a!='y':
        print('cancelled')
        return
    args = ""
    args+= "from django.contrib.auth.models import User\n"
    args+= "from utils.User import change_password as f\n"
    args+= "f('%s','%s')" % (netid, new_password)
    print(args)
    with open ('input.txt','w') as f:
        f.write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

def make_status(week):
    args = ""
    args+= "from simple_judge.models import Student, Question \n"
    args+= "from utils.User import check_user_data as f\n"
    args+= "f("+str(week)+")"
    with open ('input.txt','w') as f:
        f.write(args)
    ain=open('input.txt','r')
    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)

def execute():
    # load or dump question from each week
    if sys.argv[1] in first_command: #week1 or week2 or week3 ...
        if '-dump'  in sys.argv:
            DumpQuestion(sys.argv[1])
        elif '-v2' in sys.argv:
            LoadQuestion(sys.argv[1], 2)
        else:
            LoadQuestion(sys.argv[1])
        return

    # update simple question
    if sys.argv[1]=='update':
        LoadQuestion(sys.argv[2],3) # python3 shell.py update 102
        return
    # Export one single question from the db.
    # if sys.argv[1]=='export':


    if sys.argv[1]== 'assign':
        if len(sys.argv)==2:
            AssignQuestion()
            return
        if len(sys.argv)==3:
            AssignQuestion(sys.argv[2])
            return 

    if sys.argv[1]=='create_user':
        #net_id, student_name, (level=0)
        if len(sys.argv)==4:
            CreateUser(sys.argv[2],sys.argv[3],0 )
            return
        if len(sys.argv)==5:
            CreateUser(sys.argv[2],sys.argv[3],sys.argv[4] )
            return
    if sys.argv[1]=='import_user':
        ImportUser()
        return
    if sys.argv[1]=='change_password_yaml':
        change_password_yaml()
        return

    if sys.argv[1]=='change_password':
        change_passowrd(sys.argv[2],sys.argv[3])
        return 

    if sys.argv[1]=='status':
        if len(sys.argv)==2:
            print("Please input the the correct week")
        else:
            make_status(sys.argv[2])
        return



if __name__=='__main__':
     execute()

     print()
