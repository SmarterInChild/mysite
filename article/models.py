from django.db import models
from django.utils import timezone
from slugify import slugify
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class ArticleTag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_articletag_userid")
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.tag


class ArticleColumn(models.Model):
    user = models.ForeignKey(User, related_name='user_articlecolumn_userid', on_delete=models.CASCADE)
    column = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.column

class ArticlePost(models.Model):
    author = models.ForeignKey(User, related_name="user_article_userid", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    column = models.ForeignKey(ArticleColumn, related_name="user_article_columnid", on_delete=models.DO_NOTHING)
    body = models.TextField()
    users_like = models.ManyToManyField(User, related_name="user_article_like", blank=True)
    article_tag = models.ManyToManyField(ArticleTag, related_name="articletags", blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated',]
        index_together = [('id', 'slug'),] 

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(ArticlePost, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('article:list_article_detail', args=[self.id, self.slug])

class Comment(models.Model):
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="articlepost_comment_articlepostid")
    commentator = models.CharField(max_length=90)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created',]

    def __str__(self):
        return "Comment by {0} on {1}".format(self.commentator, self.article)


