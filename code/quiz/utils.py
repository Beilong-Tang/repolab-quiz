# Put the function Here
from django.contrib.auth.models import User
from simple_judge.models import Questiondict
from django.http import HttpResponse
import subprocess ,os,datetime
import shutil
import random
### Clean the output for the code
clean_output=True

## Check Answer for Fill in the blank questions
def checkanswer(input_sets,question_id,question_type,student_name):
    if question_type=='blank':
        return checkanswer_blank(input_sets,Questiondict.objects.get(question_id=question_id).question_content.get('answers'))
    if question_type=='mult':
        return checkanswer_mult(input_sets,Questiondict.objects.get(question_id=question_id).question_content.get('answers'))
    if question_type=='code':
        return check_answer_code(Questiondict.objects.get(question_id=question_id).question_content,input_sets,student_name)



def checkanswer_blank(input_sets, answer_sets):
    if len(input_sets)!=len(answer_sets):
        return False
    for i in range(0,len(input_sets)):
        if input_sets[i].lower().lstrip(' ').rstrip(' ')!=answer_sets[i].lower():
            return False
    return True
## Check Answer for multi choice questions
def checkanswer_mult(input_sets,answer_sets):    

    #input_sets=list (filter (lambda x : x!='',input.split(' ')))
    answer_arrays=[]
    for i in range(0,len(answer_sets)):
        if answer_sets[i]=='True':
            answer_arrays.append(i+97)
    # print(answer_arrays)
    try:
        input_answer=[ ord(char.lower()) for char in input_sets]
    except:
        return False
    return sorted(input_answer)==sorted(answer_arrays)

def checkuser(username,user_id):
    user_web = User.objects.get(pk=user_id)
    if (username!=user_web.username):
        return HttpResponse("You are not allowed to See the Page") 
    
def checktime(question_due_dict):
    due_dict_after={}
    
    tim=datetime.datetime.utcnow() # UTC
    for i, j in question_due_dict.items():
        time_start= datetime.datetime.strptime(j[0],'%Y-%m-%d %H:%M') # UTC+8
        time_end= datetime.datetime.strptime(j[1],'%Y-%m-%d %H:%M') # UTC+8
        if tim > time_end-datetime.timedelta(hours=8):
            due_dict_after[i]=[False,time_end] ## passed
        elif tim > time_start-datetime.timedelta(hours=8):
            due_dict_after[i]=[True,time_end] ## open
            #due_dict_after[i]=[True,time_end] ## open
    return due_dict_after
        
def getanswer(request, len,question_type):
    answers=[]
    if question_type=='mult':
        return list(filter(lambda x: x!="",request.POST.get('0').split(' ')))
    for i in range(0,len):
        answers.append(request.POST.get((str)(i)) if request.POST.get((str)(i))!=None else "None")
    return answers

def check_answer_code(jsonfile, answer,student_name):

    ### This is for local use
    ###
    # Get the code
    # Alice_LargestString_code
    code_path=os.getcwd()+'/coding_div'
    file2=student_name+'_'+jsonfile['title']+'_'+'code'
    filename=code_path+'/'+file2
    code=jsonfile['code']
    for i in range(0,len(answer)):
        code=code.replace('__'+(str)(i)+'__',answer[i])
    if file2 not in os.listdir(code_path):
        os.mkdir(filename)
    #code_file=open('quiz-gen/'+self.data['title']+'.txt','w')
    code_file=open(filename+'/'+jsonfile['title']+'.txt','w')
    code_file.write(code)
    code_file.close()
    # Get the checking method #jsonfile['check']
    check_file=open(filename+'/'+'check.txt','w')
    check_file.write(jsonfile['check'])
    check_file.close()
    # Get the instruction
    instruction_file=open(filename+'/'+'instruction.txt','w')
    # Replace the Json File
    jsonfile['instruction']=jsonfile['instruction'].replace('quiz-gen', 'coding_div/'+file2)
    #
    instruction_file.write(jsonfile['instruction'])
    instruction_file.close()
    ain = open(filename+'/instruction.txt','rb') # fixed by lj -- remove use of /bin/more
    p2=subprocess.Popen(args='jshell',shell=True,stdin=ain,stdout=subprocess.PIPE)
    output_file=open(filename+'/data.txt.save','wb')
    output_file.write(p2.stdout.read()) # fixed by lj -- remove use of nano
    output_file.close()
    output_file=open(filename+'/data.txt.save','r')
    ## Ready to check answers
    if jsonfile['main_output']!=None:
        main_output=jsonfile['main_output'].lstrip('\n').rstrip('\n').split()
        content=output_file.read()
        content=content[content.find('check()'):]
        for item in main_output:
            if content.find(item)!=-1:
                content=content[content.find(item)+len(item):]
            else:
                if clean_output !=False:
                    clean_all(filename)
                return False
        if clean_output !=False:
            clean_all(filename)
        return True
    else:
        for line in output_file.readlines():
            if line.find('check()true')!=-1:
                if clean_output !=False:
                    clean_all(filename)
                return True
        if clean_output !=False:
            clean_all(filename)    
        return False


def clean_all(filename):
    shutil.rmtree(filename)



def findid(question_id , question_array_length):
    if str(question_id)[1:]=='01':
        return [question_id, question_id+1]
    if str(question_id)[1:]==str(question_array_length):
        return [question_id-1, question_id]
    return [question_id-1,question_id+1]

def get_progress(question_set, length):
    # week 5, 1 2 3 4 5 
    total_array=[]
    passed_array=[]
    for i in range(1,length+1):

        total_count=0
        passed_count=0
        week_question_sets=question_set.filter(question_id__gte=100*i , question_id__lte=100*(i+1))

        for j in week_question_sets:
            if j.ifpassed == True or j.submission_times==0 :
                total_count+=1
                if j.ifpassed == True:
                    passed_count+=1
        total_array.append(str(total_count)+'/'+str(len(week_question_sets)))
        passed_array.append(str(passed_count)+'/'+str(len(week_question_sets)))
    return total_array, passed_array

def check_time(time_start, time_end):
    time_start = datetime.datetime.strptime(time_start,'%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    time_end = datetime.datetime.strptime(time_end,'%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8)))
    time_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    if time_now < time_start:
        return 0 ## not-open
    elif time_now <= time_end:
        return 1 ## open
    else:
        return -1 ## pass the due


def mult_answer_convert(mult_answer_sets):
    # ['True','False','True',]
    answer_arrays=[]
    for i in range(0,len(mult_answer_sets)):
        if mult_answer_sets[i]=='True':
            answer_arrays.append(chr(i+97))
    return answer_arrays 

def shuffle_choices(choices:list,seed : int,shuffle=True,) -> dict:
    if shuffle==True:
        random.seed(seed)
        random.shuffle(choices)
    choice_dict={}
    #['B. ababbabb', 'A. bbabaaba', 'C. bbabbbaa ']
    for index, item in enumerate(choices):
        choice_str:str = item[:item.find('.')].lstrip(' ').rstrip(' ')
        choice_dict[choice_str.lower()] = item.replace(choice_str,chr(97+index),1)
    # print(choice_dict)
    return choice_dict
    pass