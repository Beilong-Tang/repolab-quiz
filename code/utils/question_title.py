# This file is to modify the question_title in a clearer way

from simple_judge.models import Question, Student, Questiondict
import re

'''
from simple_judge.models import Question, Student, Questiondict
from utils.question_title import question_title_modify as qtm
qtm()
'''

r_code='[_][\d]+[.]'
r_blank='_quiz.[\d]+.'
r_mult='_mult.[\d]+.'

def question_title_modify():
    for q in Questiondict.objects.all():
        q.question_title=question_title_change(q.question_title,q.question_type)
        q.save()


def question_title_change(question_title,question_type):
    if question_type=='blank':
        return blank_question_title_change(question_title)
    if question_type=='mult':
        return mult_question_title_change(question_title)
    if question_type=='code':
        return code_question_title_change(question_title)

def blank_question_title_change(question_title):
    m=re.findall(r_blank,question_title)[0]
    question_title=question_title[:question_title.find('.qz.blank')].replace(m,': ').replace('c','C',1)
    return question_title

def mult_question_title_change(question_title):
    m=re.findall(r_mult,question_title)[0]
    question_title=question_title[:question_title.find('.qz.mult')].replace(m,': ').replace('c','C',1)
    return question_title

def code_question_title_change(question_title):
    m=re.findall(r_code,question_title)[0]
    question_title=question_title[:question_title.find('.code.qz')].replace(m,': ').replace('chap','Chap',1)#.capitalize())
    return question_title
