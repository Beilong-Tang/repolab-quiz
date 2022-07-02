from django.urls import path

from . import views

app_name='simple_judge'

urlpatterns = [
    path("", views.index, name="index"),
    #path("search", views.search, name="search"),
    path('signup',views.signup,name='signup'),
    path('signin',views.signin,name='signin'),
    path('signout',views.signout,name='signout'),
    #path("middleware", views.middleware, name="middleware"),
    


]

