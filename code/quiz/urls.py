from django.urls import path

from . import views

app_name='quiz'

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:user_id>/index/', views.userface,name='userface'),
    #path('<int:user_id>/index/<str:question_title>/', views.quiz, name='quiz'),
    path('quiz/index/<int:week>/<str:question_title>/', views.quiz_new, name='quiz_new'),
    path('<int:user_id>/index/<str:question_title>/checking/', views.check, name='check')

]
