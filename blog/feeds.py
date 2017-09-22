# coding=utf-8
# RSS订阅

from django.contrib.syndication.views import Feed
from .models import Post

class AllPostsRssFeed(Feed):
    title = "当然我梦想远方"
    link = "/"
    description = "当然我梦想远方测试"

    def items(self):
        return Post.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
