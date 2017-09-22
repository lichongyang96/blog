# coding=utf-8
from django.db.models.aggregates import Count
from ..models import Post, Category, Tag
from django import template


register = template.Library()


# 获取最新文章列表
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


# 按时间对文章进行归档
@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


# 分类类别列表
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 标签列表
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


