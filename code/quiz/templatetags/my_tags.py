from django import template
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
