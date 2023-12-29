from django.contrib import admin
from .models import MainThread, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(MainThread)
class MainThreadAdmin(SummernoteModelAdmin):
    list_display = ('game_id', 'name', 'status', 'created_date')
    search_fields = ['name', 'summary']
    list_filter = ('status', 'created_date')
    prepopulated_fields = {'slug': ('name',)}
    summernote_fields = ('summary',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'game_id', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('user__username', 'text')
