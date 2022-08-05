from django.urls import path

from . import views

app_name='forum'

urlpatterns = [
    path('', views.forum,name='forum'),
    path('/<int:id>:<int:roll>',views.forum_post,name='forum_post'),
    path('/create',views.create_post,name='create_post'),
]