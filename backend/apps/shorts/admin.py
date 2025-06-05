from django.contrib import admin

from .models.comment import Comment
from .models.follow import Follow
from .models.like import Like
from .models.report import Report
from .models.tag import Tag
from .models.video import Video
from .models.view import View


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Tag._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    list_display_links = list_display
    ordering = ("-id",)
    list_filter = []
    search_fields = ["name"]
    list_per_page = 16


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Video._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    list_display_links = list_display
    ordering = ("-updated_at",)
    list_filter = ["privacy", "created_at", "updated_at"]
    search_fields = ["title"]
    list_per_page = 16


@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in View._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    list_display_links = list_display
    ordering = ("-timestamp",)
    list_filter = ["timestamp"]
    search_fields = []
    list_per_page = 16


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Like._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    list_display_links = list_display
    ordering = ("-liked_at",)
    list_filter = ["liked_at"]
    search_fields = []
    list_per_page = 16


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Comment._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    list_display_links = list_display
    ordering = ("-updated_at",)
    list_filter = ["comment_at", "updated_at"]
    search_fields = ["content"]
    list_per_page = 16


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Follow._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    list_display_links = list_display
    ordering = ("-followed_at",)
    list_filter = ["followed_at", "followed_at"]
    search_fields = []
    list_per_page = 16


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        field.name
        for field in Report._meta.get_fields()
        if not (field.many_to_many or field.one_to_many)
    ]
    list_display_links = list_display
    ordering = ("-updated_at",)
    list_filter = ["status", "created_at", "updated_at"]
    search_fields = ["reason"]
    list_per_page = 16
