# Put the function Here
from django.contrib.auth.models import User
from simple_judge.models import Questiondict
from django.http import HttpResponse
import subprocess ,os,datetime,re
import shutil

### Clean the output for the code
clean_output=False
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
        if input_sets[i]!=answer_sets[i]:
            return False
    return True
## Check Answer for multi choice questions
def checkanswer_mult(input_sets,answer_sets):    

    #input_sets=list (filter (lambda x : x!='',input.split(' ')))
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
    
def checktime():

    # week=['2022-8-21 23:59','2022-8-28 23:59','2022-9-4 23:59','2022-9-11 23:59',
    # '2022-9-18 23:59','2022-9-25 23:59','2022-10-2 23:59','2022-10-9 23:59']

    ## Test Week
    week=['2022-7-13 23:59','2022-7-14 23:59','2022-9-4 23:59','2022-9-11 23:59',
    '2022-9-18 23:59','2022-9-25 23:59','2022-10-2 23:59','2022-10-9 23:59']

    tim=datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    # 0 - 6 
    for i in range(0, len(week)-1):
        time_start= datetime.datetime.strptime(week[i],'%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8))) # UTC+8
        time_end= datetime.datetime.strptime(week[i+1],'%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8))) # UTC+8
        if (tim>time_start and tim < time_end):
            return i+1
    return 8

def getanswer(request, len,question_type):
    answers=[]
    if question_type=='mult':
        return list(filter(lambda x: x!="",request.POST.get('0').split(' ')))
    for i in range(0,len):
        answers.append(request.POST.get((str)(i)))
    return answers

def check_answer_code(jsonfile, answer,student_name):
    running_directory=os.getcwd()+'/utils'
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