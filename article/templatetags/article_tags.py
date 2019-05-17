import markdown
from django import template
from article.models import ArticlePost
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag
def total_articles():
    return ArticlePost.objects.count()

@register.simple_tag
def author_total_articles(user):
    return user.user_article_userid.count()

@register.inclusion_tag('article/list/latest_articles.html')
def latest_articles(n=5):
    latest_articles = ArticlePost.objects.order_by('-created')[:n]
    return {"latest_articles": latest_articles}

# simple_tag应该还是不能返回list
# @register.simple_tag
# def most_comment_articles(n=3):
#     return most_comment_articles = ArticlePost.objects.annotate(total_comments=Count('articlepost_comment_articlepostid')).order_by('-total_comments')[:n]

@register.filter(name='markdown')
def markdown_filter(text):
    return mark_safe(markdown.markdown(text))