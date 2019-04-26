from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm 

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        login_form = LoginForm(post_dict)
        if login_form.is_valid():
            auth_user = authenticate(request, username=post_dict['username'], password=post_dict['password'])
            #auth_user = authenticate(request, username='wangdong', password='1qaz@WSXdj')
            if auth_user:
                return HttpResponse("欢迎, 你已经成功登陆")
            else:
                return HttpResponse("登录失败，用户名或密码错误")
        else:
            return HttpResponse("Invalid login")
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})

def register(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        register_form = RegistrationForm(post_dict)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(post_dict['password'])
            new_user.save()
            return HttpResponse("注册成功")
        else:
            return HttpResponse("注册失败")
    else:
        register_form = RegistrationForm()
        return render(request, "account/register.html", {"form": register_form})
