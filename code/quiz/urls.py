from django.urls import path

from . import views

app_name='quiz'

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:user_id>/index/', views.userface,name='userface'),
    path('<int:user_id>/assignment',views.assignment, name='assignment'),
    path('quiz/index/<int:question_id>/', views.quiz_new, name='quiz_new'),
    path('index/<int:question_id>/checking/', views.check, name='check'),
    path('<int:user_id>/account',views.account, name='account')
]
