from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chatView, name='chatView'),
    path('login/', views.loginView, name='loginView'),
    path('process/', views.processLoginView, name='processView'),
    path('connect/', views.connectView, name='connectView'),
    path('signup/', views.signUpView, name='signUpView'),
    path('process_login/', views.processLogIn, name='processLogIn')
]