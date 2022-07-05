import sys, os,subprocess,json

# Revise the Quiz director as where the quiz is at 
home_dir='/mnt/c/Users/Beilong Tang/Desktop/Main/CODE/DJANGO_new/repolab-quiz/bank'
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
    args+=delete_all()
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
                    quiz_title=quiz_path[quiz_path.find('princeton-book')+15:].replace('quiz-gen/','').replace('/','_')
                    #print(quiz_title)
                    quiz_dict[quiz_title]=quiz_path
                    args+="Questiondict(question_type='blank',question_title= '"+quiz_title+"',question_content={'de':1}).save()\n"
    for i,j in quiz_dict.items():
        args+="q=Questiondict.objects.get(question_title='"+i+"')\n"
        args+="q.question_content=json.load(open('"+j+"','r'))\n"
        args+='q.save()\n'
    open('input.txt','w').write(args)
    ain=open('input.txt','r')




    p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)
    


    pass
        #print(os.listdir(i))

def delete_all():
    return 'Questiondict.objects.all().delete()\n'
    

pass

if __name__=='__main__':
    if sys.argv[1]=='blank':
        x=generate_input_file_blank()
    
    #open('input.txt','w').write(x)
    #ain=open('input.txt','r')
    ## This will run the process of storing the data
    #p1= subprocess.Popen(args='python3 manage.py shell',shell=True, stdin=ain)
    #os.system(args)