from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm , UserProfileForm, UserInfoForm, UserForm
from .models import UserProfile, UserInfo
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
import base64

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        login_form = LoginForm(post_dict)
        if login_form.is_valid():
            auth_user = authenticate(request, username=post_dict['username'], password=post_dict['password'])
            #auth_user = authenticate(request, username='wangdong', password='1qaz@WSXdj')
            #test send mail
            status = send_mail('test send mail','user user126 login',settings.DEFAULT_FROM_EMAIL,['126126126@126.com'],html_message='hello',fail_silently=False)
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
        userprofile_form = UserProfileForm(post_dict)
        if register_form.is_valid() and userprofile_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(post_dict['password'])
            new_user.save()
            new_userprofile = userprofile_form.save(commit=False)
            new_userprofile.user = new_user
            new_userprofile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponse("注册成功")
        else:
            return HttpResponse("注册失败")
    else:
        register_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": register_form, "profile":userprofile_form})

@login_required(login_url='/account/login')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request, "account/myself.html", {"user": user, "userprofile": userprofile, "userinfo": userinfo})

@login_required(login_url='/account/login')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)

    if request.method == 'POST':
        post_dict = request.POST.dict()
        user_form = UserForm(post_dict)
        userprofile_form = UserProfileForm(post_dict)
        userinfo_form = UserInfoForm(post_dict)
        if user_form.is_valid() and userprofile_form.is_valid() and userinfo_form.is_valid():
            user.email = post_dict['email']
            userprofile.birth = post_dict['birth']
            userprofile.phone = post_dict['phone']
            userinfo.school = post_dict['school']
            userinfo.company = post_dict['company']
            userinfo.profession = post_dict['profession']
            userinfo.address = post_dict['address']
            userinfo.aboutme = post_dict['aboutme']
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth": userprofile.birth, "phone": userprofile.phone})
        userinfo_form = UserInfoForm(instance=userinfo)
        return render(request, "account/myself_edit.html", {"user_form": user_form, "userprofile_form": userprofile_form, "userinfo_form": userinfo_form})


#如果发送给图片发送后端是二进制数据可以如下处理
# @login_required(login_url='/account/login')
# @csrf_exempt
# def my_image(request):
#     if request.method == 'POST':
#         post_dict = request.POST.dict()
#         photo_name = request.user.username + '.png'
#         userinfo = UserInfo.objects.get(user=request.user.id)
#         userinfo.photo = ContentFile(post_dict['photo'], name=photo_name)
#         userinfo.save()
#         return HttpResponse("1")
#     else:
#         return render(request, 'account/cropbox.html',)

#如果前段发送图片是base64编码可以如下处理
@login_required(login_url='/account/login')
@csrf_exempt
def my_image(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        header, data = post_dict['photo'].split(';base64,')
        try:
            decode_data = base64.b64decode(data)
        except TypeError:
            TypeError('invalid image') 
        photo_name = request.user.username + '.png'
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = ContentFile(decode_data, name=photo_name)
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request, 'account/cropbox.html',)

