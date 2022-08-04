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