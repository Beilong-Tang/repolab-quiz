from django.urls import path

from . import views

app_name='quiz'

urlpatterns = [
    path('index/', views.userface,name='userface'),
    path('assignment/',views.assignment, name='assignment'),
    path('quiz/<int:question_id>/', views.quiz_new, name='quiz_new'),
    path('index/<int:question_id>/checking/', views.check, name='check'),
    path('account/',views.account, name='account')
]
