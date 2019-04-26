from django.urls import path
#from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    #path('login/', views.user_login, name="user_login"),
    path('new_login/', auth_views.LoginView.as_view(template_name="account/login.html")),
    path('login/', auth_views.LoginView.as_view(), name="user_login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="user_logout"),
]