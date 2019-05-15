from django.urls import path
from . import views, list_views

app_name = 'article'
urlpatterns = [
    path('article-column/', views.article_column, name="article_column"),
    path('rename-column/', views.rename_column, name="rename_article_column"),
    path('del-column/', views.delete_column, name="del_article_column"),
    path('article-post/', views.article_post, name="article_post"),
    path('article-list/', views.article_list, name="article_list"),
    path('article-detail/<id>/<slug>/', views.article_detail, name="article_detail"),
    path('redit-article/<article_id>/', views.redit_article, name="redit_article"),
    path('del-article/', views.delete_article, name="del_article"),

    path('list-article-titles/', list_views.article_titles, name="article_titles"),
    path('list-article-titles/<username>/', list_views.article_titles, name="article_titles"),
    path('list-article-detail/<id>/<slug>/', list_views.article_detail, name="list_article_detail"),
    path('like-article', list_views.like_article, name="like_article"),
]
