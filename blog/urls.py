import django.contrib.auth.views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path,include
from . import views
app_name='blog'

urlpatterns=[
    path('top/',views.top_page, name="top"), # リダイレクト
    url( r'^login/$',auth_views.LoginView.as_view(template_name="user_auth/login.html"), name="login"),
    url( r'^logout/$',auth_views.LogoutView.as_view(template_name="user_auth/login.html"), name="logout"),
    #path('login_complete/',views.top_page, name="login_complete"),
    path('<slug>/', views.my_page, name="my_page"),
]
