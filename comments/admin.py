from django.contrib import admin
from comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "article", "text", "created_at")
    search_fields = ("author__username", "article__title", "text")
