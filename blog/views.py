# coding=utf-8

import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Q
# Create your views here.


# 主页类视图
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # 分页
    paginate_by = 2



# # 主页
# def index(request):
#     post_list = Post.objects.all().order_by('-create_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# 文章详情页视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm
        comment_list = self.object.comments_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


# 文章详情页
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.body = markdown.markdown(post.body, extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         'markdown.extensions.toc',
#     ])
#     post.increase_views()
#     form = CommentForm()
#     comment_list = post.comments_set.all()
#     context = {
#         'post': post,
#         'form': form,
#         'comment_list': comment_list
#     }
#     return render(request, 'blog/detail.html', context=context)


# 按时间显示文章视图
class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year, create_time__month=month,)


# 按时间显示文章
# def archives(request, year, month):
#     post_list = Post.objects.filter(
#         create_time__year=year,
#         create_time__month=month,
#     ).order_by('-create_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


# 按分类显示文章视图
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


# 按标签显示文章视图
class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tag=tag)


# 搜索
def search(request):
    q = request.GET.get('q')
    error_msg = ""
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                                   'post_list': post_list})

# # 按分类显示文章
# def category(request, pk):
#     cate = get_object_or_404(Category, pk=pk)
#     post_list = Post.objects.filter(
#         category=cate
#     ).order_by('-create_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})





