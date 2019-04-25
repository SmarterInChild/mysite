from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm 

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        login_form = LoginForm(post_dict)
        print
        if login_form.is_valid():
            auth_user = authenticate(request, username=post_dict['username'], password=post_dict['password'])
            #auth_user = authenticate(request, username='wangdong', password='1qaz@WSXdj')
            if auth_user:
                return HttpResponse("Welcome, you have been authencicated successfully")
            else:
                return HttpResponse("Sorry, your username or password is not correct")
        else:
            return HttpResponse("Invalid login")
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})
