from django.contrib import admin
from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    exclude = ['slug']


admin.site.register(Article, ArticleAdmin)
