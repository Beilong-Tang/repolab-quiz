from django.urls import path

from . import views

app_name='simple_judge'

urlpatterns = [
    path("", views.index, name="index"),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    path('change_password',views.change_password,name='change_password'),
]

