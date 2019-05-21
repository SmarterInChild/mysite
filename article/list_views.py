import redis
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ArticleColumn, ArticlePost, Comment
from .forms import CommentForm

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

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
    total_views = r.incr("article:{}:views".format(article.id))
    #r.zincrby(name='article_ranking', amount=1, value=article.id)
    r.zincrby('article_ranking', 1, article.id)


    article_ranking = r.zrange('article_ranking', 0, -1, desc=True)[:10]
    article_ranking_ids = [int(id) for id in article_ranking]
    most_viewed = list(ArticlePost.objects.filter(id__in=article_ranking_ids))
    most_viewed.sort(key=lambda x: article_ranking_ids.index(x.id))

    most_comments = ArticlePost.objects.annotate(total_comments=Count('articlepost_comment_articlepostid')).order_by('-total_comments')[:3]

    article_tags_ids = article.article_tag.values_list('id', flat=True)
    similar_articles = ArticlePost.objects.filter(article_tag__in=article_tags_ids).exclude(id=article.id)
    similar_articles = similar_articles.annotate(same_tag=Count("article_tag")).order_by('-same_tag', '-created')[:4]

    if request.method == 'POST':
        post_dict = request.POST.dict()
        comment_form = CommentForm(post_dict)
        if comment_form.is_valid():
            new_comment = Comment()
            new_comment.article = article
            new_comment.commentator = post_dict['commentator']
            new_comment.body = post_dict['body']
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, "article/list/article_detail.html", {"article": article, "total_views": total_views, "most_viewed": most_viewed, "comment_form": comment_form, "most_comments": most_comments, "similar_articles":similar_articles})

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