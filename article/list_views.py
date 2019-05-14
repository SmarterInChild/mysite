from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from .models import ArticleColumn, ArticlePost

def article_titles(request, username=None):
    if username:
        user = User.objects.get(username=username)
        try:
            userinfo = user.userinfo
        except:
            userinfo = None  
        article_titles = ArticlePost.objects.filter(author=user)
    else:
        article_titles = ArticlePost.objects.all()
    paginator = Paginator(article_titles, 5)
    page = request.GET.get('page')
    try:
        current_page = paginator.get_page(page)
        articles = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.get_page(1)
        articles = current_page.object_list
    except EmptyPage:
        current_page = paginator.get_page(paginator.num_pages)
        articles = current_page.object_list
    if username:
        return render(request, "article/list/user_article_titles.html", {"articles": articles, "page": current_page, "user": user, "userinfo": userinfo})
    return render(request, "article/list/article_titles.html", {"articles": articles, "page": current_page})

def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/list/article_detail.html", {"article": article})