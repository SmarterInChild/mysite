from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.blog_title, name="blog_title"),
    path('<int:article_id>/', views.blog_content, name="blog_content"),
]
