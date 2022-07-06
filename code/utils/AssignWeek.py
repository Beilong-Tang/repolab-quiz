# This file is to assign the quiz for the current week
# For example: If we do assign()week
# Then, the quiz will be euqally distributed in the week
# For example, if we do assignweek(week=3, chap=2, section="2.1"),
# It will assign the current quiz to the specific week chapter2, section 2.1)
# 



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