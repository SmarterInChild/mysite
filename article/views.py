from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ArticleColumn
from .forms import ArticleColumnForm
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