# coding=utf-8

# 用于管理不同网址对应的不同处理函数

from django.conf.urls import url
from . import views


app_name = 'comments'
urlpatterns = [
    url(r'^comment/post/(?P<post_pk>[0-9]+)/$', views.post_comment, name='post_comment'),
]