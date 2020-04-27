from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'author',
                    'just_users', 'created_at', 'updated_at')
    list_display_links = ('id', 'title')
    list_filter = ('category', 'author',
                   'just_users', 'created_at', 'updated_at')
    list_per_page = 10
    search_fields = ('id', 'title', 'category', 'author')


admin.site.register(Post, PostAdmin)
