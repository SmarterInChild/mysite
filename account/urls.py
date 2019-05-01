from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'
urlpatterns = [
    #path('login/', views.user_login, name="user_login"),
    path('new-login/', auth_views.LoginView.as_view(template_name="account/login.html")),
    path('login/', auth_views.LoginView.as_view(), name="user_login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logout.html"), name="user_logout"),
    path('register/', views.register, name="user_register"),
    # path('password-change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    # path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html", success_url=reverse_lazy('account:password_change_done')), name="password_change"),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name="password_change_done"),
    #重置密码测试，必须有用户用这个邮箱注册过才可以调用这个PasswordResetView，否则不会有任何响应，官网说这是为了防止潜在的信息泄露
    path('password-reset/', auth_views.PasswordResetView.as_view(
        email_template_name='account/password_reset_email.html',
        subject_template_name='account/password_reset_subject.txt',
        success_url=reverse_lazy('account:password_reset_done'),
        template_name='account/password_reset_form.html',
    ), name="password_reset"),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html', success_url=reverse_lazy('account:password_reset_complete')), name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), name="password_reset_complete" ),
    path('my-information/', views.myself, name="my_information"),
    path('edit-my-information/', views.myself_edit, name="edit_my_information"),
    path('my-image/', views.my_image, name="my_image"),
]