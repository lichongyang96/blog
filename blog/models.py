# coding=utf-8
from __future__ import unicode_literals
import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
# Create your models here.


# 分类数据库
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 标签数据库
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 文章数据库
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    create_time = models.DateTimeField()
    modify_time = models.DateTimeField()
    # 文章摘要
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category)
    tag = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)
    # 文章阅读量
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)