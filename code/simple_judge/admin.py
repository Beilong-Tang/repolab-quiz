from django.contrib import admin

from django.contrib.auth.models import User
from .models import Student,Question,Questiondict
# Register your models here.

class QuestionInline(admin.TabularInline):
    model=Question
    extra=3

class StudentAdmin(admin.ModelAdmin):

    inlines=[QuestionInline]


admin.site.register(Student, StudentAdmin)
admin.site.register(Question)
admin.site.register(Questiondict)