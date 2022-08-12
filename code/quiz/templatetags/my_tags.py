from django import template
import datetime

register=template.Library()

@register.filter
def last2(question_id):
    x = str(question_id)
    return x[1:]

@register.filter 
## Pass for False, open for true
def status(status_boolean):
    if status_boolean:
        return 'Open'
    else:
        return 'Closed'

@register.filter
def answer(answers):
    answer_string=""
    for i in range(0,len(answers)):
        answer_string+="_("+str(i)+")_: "+answers[i]+"\n"
    return answer_string
    return "\n".join(answers)

@register.filter
def mult_answer(answers):
    return " ".join(answers)

@register.filter
def date(date):
    return date.date()

@register.filter
def show_category(level):
    if level==0:
        return 'Week1'
    if level==1:
        return 'Week2'
    if level==2:
        return 'Week3'
    if level==3:
        return 'Week4'
    if level==4:
        return 'Week5'
    if level==5:
        return 'Week6'
    if level==6:
        return 'Week7'
    
@register.filter
def show_question(question_id):
    s = str(question_id)[1:]
    return 'Problem'+s

## Name 
@register.filter
def title1(name):
    if name[0:2]!='We' and name[0:2]!='St' and name[0:2]!='Al':
        return 'Week' + str(name[0:1])
    return name

@register.filter
def title2(name):
    if name[0:2]=='We':
        return 'All'
    return 'Problem' + str(int(name[1:]))

@register.filter
def cap(name):
    return name[0:1]