from django import template
register=template.Library()

@register.filter
def last2(question_id):
    x = str(question_id)
    return x[1:]

