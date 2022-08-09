from django.urls import path, re_path

from . import views

app_name='forum'

urlpatterns = [
    path('/<str:filt>', views.forum,name='forum'),
    path('<int:id>:<int:roll>?<int:textroll>/<str:filt>',views.forum_post,name='forum_post'),
    path('create',views.create_post,name='create_post'),
    path('save_star/<int:id>/<int:roll>/<str:filt>',views.save_star,name='save_star'),
    path('<int:id>/<int:roll>/:<int:textroll>/<str:filt>',views.save_comment,name='save_comment')
]