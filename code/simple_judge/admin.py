from django.contrib import admin

from django.contrib.auth.models import User
from .models import Student,Question,Questiondict
# Register your models here.

class QuestionInline(admin.TabularInline):
    model=Question
    extra=3

class StudentAdmin(admin.ModelAdmin):

    inlines=[QuestionInline]
   # list_display=('')

class QuestiondictAdmin(admin.ModelAdmin):

    list_display=('question_id','question_type','question_title','question_level','question_week')

admin.site.register(Student, StudentAdmin)
admin.site.register(Question)
admin.site.register(Questiondict,QuestiondictAdmin)