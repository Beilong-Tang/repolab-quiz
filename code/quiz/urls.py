from django.urls import path

from . import views

app_name='quiz'

urlpatterns = [
    path("", views.index, name="index"),
    path('<int:user_id>/index/', views.userface,name='userface')

]
