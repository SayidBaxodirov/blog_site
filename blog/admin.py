from django.contrib import admin

from blog.models import Post, Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'slug', 'publish_date', 'status')
    list_filter = ('status', 'publish_date', 'author', 'create_date')
    search_fields = ('author', 'title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish_date'
    ordering = ('status', 'publish_date')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'body', 'active')
    list_filter = ('author', 'post', 'active')
