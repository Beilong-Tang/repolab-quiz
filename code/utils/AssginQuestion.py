# This file is to assign the quiz for the current week
# For example: If we do assign()week
# Then, the quiz will be euqally distributed in the week
# For example, if we do assignweek(week=3, chap=2, section="2.1"),
# It will assign the current quiz to the specific week chapter2, section 2.1)
# 
'''
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    question_title=models.CharField(max_length=50)
    question_id=models.IntegerField(default=0)
    ifpassed=models.BooleanField('ifpassed')
    pub_date=models.DateTimeField('date published', default=datetime.datetime.strptime('2022-7-13 23:59','%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8))))
    due_date=models.DateTimeField('date due', default=datetime.datetime.strptime('2022-7-14 23:59','%Y-%m-%d %H:%M').astimezone(datetime.timezone(datetime.timedelta(hours=8))))
    logx=models.TextField()
    submission_times=models.IntegerField(default=5)'''
'''


question_id
ifpassed
logx
pub_date
due_date
submission_times
question_title
'''




import random

from simple_judge.models import Student, Question, Questiondict
from utils.settings import question_due_dict as question_due
def AssignQuestion(student_netid=""):
    ## Gather all the id
    id_all =[]
    for q in Questiondict.objects.all():
        id_all.append(q.question_id)

    if student_netid=="":
    ## All the student
        for s in Student.objects.all():

            ## question_dict_due
            if s.question_due_dict['week1'][0]=='2022-7-29 6:00':
                s.question_due_dict=question_due
                s.save()
                pass

            id_student=[]
            for q in s.question_set.all():
                id_student.append(q.question_id)


            for id in id_all:
                if id not in id_student:
                    q = s.question_set.create(question_id=id,
                                            question_title=Questiondict.objects.get(question_id=id).question_title,
                                            seed = random.randint(0,100))
                    q.save()
            print(s.student_netid,' finished')
    else:
        s= Student.objects.get(student_netid=student_netid)

            ## question_dict_due
        if s.question_due_dict['week1'][0]=='2022-7-29 6:00':
            s.question_due_dict=question_due
            s.save()
            pass

        id_student=[]
        for q in s.question_set.all():
            id_student.append(q.question_id)


        for id in id_all:
            if id not in id_student:
                q = s.question_set.create(question_id=id,
                                        question_title=Questiondict.objects.get(question_id=id).question_title,
                                        seed = random.randint(0,100))
                q.save()
        print('finished')

# This function will return an args
def assign_week_main(default=True, week=0, chap=0, section="0"):
    return assign_week_default() if default==True else assign_week_specific(week, chap, section)
    pass

def assign_week_default():
    args="from simple_judge.models import Questiondict\n"
    args+="for q in Questiondict.objects.all():\n"
    args+="    chap=q.question_title[q.question_title.find('chap')+4:q.question_title.find('chap')+6]\n"
    args+="    q.question_week=(int)(chap)\n"
    args+="    q.save()\n"
    return args
    pass

def assign_week_specific(week, chap,section):
    args="from simple_judge.models import Questiondict\n"
    args+="for q in Questiondict.objects.all():\n"
    args+="    if q.question_title.find('chap0"+(str)(chap)+"')!=-1 and q.question_title.find('sec-"+section+"')!=-1:\n"
    args+="        q.question_week="+(str)(week)+"\n"
    args+="        q.save()\n"
    return args 
    pass

    





if __name__=='__main__':

    #print(assign_week_main(False, 1 ,1,'1'))
    print(assign_week_main(False,1,1,"1.1"))
    pass