from django.contrib import admin

# Register your models here.
from .models import Post,Comment
class PostAdmin(admin.ModelAdmin):
    list_display = ['id']

# admin.site.register(Post)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Post,PostAdmin)

