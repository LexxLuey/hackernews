from django.contrib import admin
from .models import Job, Story, Comment, Poll, PollOption, HackerNewsItem


class CommentInLine(admin.StackedInline):
    model = Comment


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['author', 'type', 'created', 'title', 'comment_count']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['author', 'type', 'created', 'title', 'comment_count', 'score']
    list_filter = ['created', 'score', 'comment_count']
    search_fields = ['title']
    # inlines = [CommentInLine]


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    list_filter = ['created', 'score', 'comment_count']
    search_fields = ['title']
    # inlines = [CommentInLine]


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ['comment_count', 'poll', 'score']


@admin.register(HackerNewsItem)
class HackerNewsItemAdmin(admin.ModelAdmin):
    list_display = ['author', 'type', 'created', 'title', 'comment_count', 'score']
    list_filter = ['created', 'score', 'comment_count']
    search_fields = ['title']
