from simple_judge.models import Questiondict

'''
from simple_judge.models import Question, Student, Questiondict
from utils.Code import code_modification as cm
cm()
'''



def code_modification():
    for question in Questiondict.objects.filter(question_type='code'):
        instruction=question.question_content.get('instruction')
        instruction=instruction.replace('quiz-gen','wdir-code')
        question.question_content['instruction']=instruction
        question.save()

