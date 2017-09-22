from django.contrib import admin
from .models import Category, Tag, Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modify_time', 'category', 'author']


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)