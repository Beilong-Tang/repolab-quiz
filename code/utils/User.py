## This file is to create user and change the password

from simple_judge.models import Student
from django.contrib.auth.models import User
from utils.settings import user_raw_path as user_raw_file
from utils.settings import password_yaml as password_yaml
import random as r
from django.db.models import Q
import yaml
import os
status_path = os.path.dirname(os.path.abspath(__file__))

## This will create a user and assign the user a foreign key to the student
def create_user(net_id, student_name, level=0):
    u = User.objects.create(username=net_id)
    password = password_random_gen()
    u.set_password(password)
    u.save()    
    s = Student(user = u, student_name=student_name.replace('_',' '),student_netid=net_id, level=level)
    s.save()
    with open ('utils/user.txt','a') as f:
        f.write(net_id+" "+student_name+" "+ password+' '+str(level)+" ;\n")
    
    authoriy_modify(s)

    print('finished')
    pass

## This is in case the studetn lost their password
def change_password(username, password):
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print('finished')
    pass

def authoriy_modify(student):
    print('Modifying authority')
    level = student.level
    if level == 1 or level == 2:
        user = student.user
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return


## This will randomly gen a password which is 8-char-length, containing all the things in the letter
def password_random_gen():
    letter= ['a','b','c','d','e','f','g','h','i',
          'j','k','l','m','n','o','p','q','r',
          's','t','u','v','w','x','y','z',
          'A','B','C','D','E','F','G','H','I',
          'J','K','L','M','N','O','P','Q','R',
          'S','T','U','V','W','X','Y','Z',
          '1','2','3','4','5','6','7','8','9']

    return "".join(r.sample(letter,8))
    

def importing_user():
    with open(user_raw_file,'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            line_array = line.split(',') #"Tang, Beilong",bt132@duke.edu,lunji.zhu@dukekunshan.edu.cn,TA#
            student_name = (line_array[1]+line_array[0]).lstrip(' ').replace('""','_')
            netid = line_array[2][0:line_array[2].find('@')]
            #print(line_array[4]==)
            level = 0 if line_array[4]=='Student' else 1 if line_array[4]=='TA' else 2
            create_user(net_id = netid, student_name= student_name, level = level)

def change_passowrd_yaml():
    password_list = yaml.load(open(password_yaml,'r').read())['passwd']
    print(password_list)
    student_netid_list = [s.username for s in User.objects.all()]
    for i in password_list:
        if i[0] in student_netid_list:
            u = User.objects.get(username = i[0])
            u.set_password(str(i[1]))
            u.save()
            print (i[0],'finished')
        else:
            print(i[0] ,'is not in the list')

def check_user_data(week):
    output = "week"+ str(week) + '\n'
    for s in Student.objects.filter(level=0):
        x = s.question_set.filter(ifpassed=True, question_id__gte=week*100,question_id__lte=(week+1)*100 ).count()
        output+=str(x) + ' , ' + s.student_name +' , ' + s.student_netid + ' , \n'
    with open (status_path+'/status.txt','w') as f:
        f.write(output)
    print('finished')


if __name__ == '__main__':
    print(status_path)