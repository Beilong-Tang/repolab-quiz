from django.urls import path, re_path

from . import views

app_name='forum'

urlpatterns = [
    path('/', views.forum,name='forum'),
    path('<int:id>:<int:roll>?<int:textroll>',views.forum_post,name='forum_post'),
    path('create',views.create_post,name='create_post'),
    path('save_star/<int:id>/<int:roll>',views.save_star,name='save_star'),
    path('<int:id>/<int:roll>/:<int:textroll>',views.save_comment,name='save_comment')
]