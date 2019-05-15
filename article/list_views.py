from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
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

@login_required(login_url='account/login')
@require_POST
@csrf_exempt
def like_article(request):
    #post_dict = request.POST.dict()
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if action and article_id:
        try:
            article = ArticlePost.objects.get(id=article_id)
            # 以下是查找user点赞过的所有article
            # articles = request.user.user_article_like.all()
            # for a in articles:
            #     print(a)
            # 以下是所有点赞该文章的用户
            # users = article.users_like.all()
            # for u in users:
            #     print(u)
            if action == "like":
                article.users_like.add(request.user)
                return HttpResponse("1")
            else:
                article.users_like.remove(request.user)
                return HttpResponse("2")
        except:
            return HttpResponse("no article")