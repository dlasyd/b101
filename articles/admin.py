from django.contrib import admin
from .models import Article, Category, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('state',)
    filter_horizontal = ('tags', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

