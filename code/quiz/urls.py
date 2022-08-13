from django.urls import path

from . import views

app_name='quiz'

urlpatterns = [
    path('index/', views.userface,name='userface'),
    path('assignment/',views.assignment, name='assignment'),
    path('quiz/<int:question_id>/', views.quiz_new, name='quiz_new'),
    path('index/<int:question_id>/checking/', views.check, name='check'),
    path('account/',views.account, name='account'),
    path('admin/',views.admin,name='admin')  ,
    path('admin/assignment',views.admin_assignment,name='admin_assignment'),
    path('admin/quiz/<str:week>',views.admin_quiz,name='admin_quiz'),
    path('message/',views.message,name='message')
]
