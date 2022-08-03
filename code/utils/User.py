## This file is to create user and change the password

from simple_judge.models import Student
from django.contrib.auth.models import User

import random as r

## This will create a user and assign the user a foreign key to the student
def create_user(net_id, student_name, student_id, level=0):
    u = User.objects.create(username=net_id)
    password= password_random_gen()
    u.set_password(password)
    u.save()    
    s = Student(user = u, student_name=student_name, student_id = student_id,student_netid=net_id, level=level)
    s.save()
    with open ('utils/user.txt','a') as f:
        f.write(net_id+" "+student_name+" "+str(student_id)+" "+ password+' '+str(level)+"\n")
    print('finished')
    pass

## This is in case the studetn lost their password
def change_password(username, password):
    u = User.objects.get(username=username)
    u.set_password(password)
    u.save()
    print('finished')

    pass



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
    
