from django.contrib import admin
from .models import ArticleCategories, Articles, UserProfile, Cities
# Register your models here.


class ArticlesAdmin(admin.ModelAdmin):
    readonly_fields = ('boughts',)


admin.site.register(UserProfile)
admin.site.register(Articles, ArticlesAdmin)
admin.site.register(ArticleCategories)
admin.site.register(Cities)
