from django.shortcuts import render, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm
# Create your views here.

@login_required(login_url='account/login')
@csrf_exempt
def article_column(request):
    if request.method == 'GET':
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns, "column_form": column_form})
    if request.method == 'POST':
        post_dict = request.POST.dict()
        column_name = post_dict['column']
        columns = ArticleColumn.objects.filter(user=request.user, column=column_name)
        if columns:
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")

@login_required(login_url='account/login')
@require_POST
@csrf_exempt
def rename_column(request):
    post_dict = request.POST.dict()
    column_name = post_dict['column_name']
    column_id = post_dict['column_id']
    try:
        column = ArticleColumn.objects.get(id=column_id)
        column.column = column_name
        column.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")

@login_required(login_url='account/login')
@require_POST
@csrf_exempt
def delete_column(request):
    post_dict = request.POST.dict()
    column_id = post_dict['column_id']
    try:
        column = ArticleColumn.objects.get(id=column_id)
        column.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url='account/login')
@csrf_exempt
def article_post(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        article_post_form = ArticlePostForm(post_dict)
        if article_post_form.is_valid():
            try:
                new_article = ArticlePost()
                new_article.title = post_dict['title']
                new_article.body = post_dict['body']
                new_article.author = request.user
                new_article.column = request.user.user_articlecolumn_userid.get(id=post_dict['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.user_articlecolumn_userid.all()
        return render(request, "article/column/article_post.html", {"article_post_form": article_post_form, "article_columns": article_columns})

@login_required(login_url='account/login')
def article_list(request):
    #articles = request.user.user_article_userid.all()
    article_list = ArticlePost.objects.filter(author=request.user)
    paginator = Paginator(article_list, 10)
    # for article in articles:
    #     print(article.get_absolute_url())
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
    return render(request, "article/column/articles.html", {"articles": articles, "page": current_page})

@login_required(login_url='account/login')
def article_detail(request, id, slug):
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article": article})


@login_required(login_url='account/login')
@csrf_exempt
def redit_article(request, article_id):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        article_post_form = ArticlePostForm(post_dict)
        if article_post_form.is_valid():
            try:
                upfate_article = ArticlePost.objects.get(id=article_id)
                upfate_article.title = post_dict['title']
                upfate_article.body = post_dict['body']
                upfate_article.author = request.user
                upfate_article.column = request.user.user_articlecolumn_userid.get(id=post_dict['column_id'])
                upfate_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    if request.method == 'GET':
        article_columns = request.user.user_articlecolumn_userid.all()
        article = ArticlePost.objects.get(id=article_id)
        article_post_form = ArticlePostForm(initial={"title": article.title})
        return render(request, "article/column/redit_article.html", {"article_post_form": article_post_form, "article_columns": article_columns, "article": article})


@login_required(login_url='account/login')
@require_POST
@csrf_exempt
def delete_article(request):
    post_dict = request.POST.dict()
    column_id = post_dict['article_id']
    try:
        article = ArticlePost.objects.get(id=column_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")