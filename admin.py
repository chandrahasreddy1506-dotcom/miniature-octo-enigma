from django.contrib import admin

from .models import Category, Comment, Issue, Region, UserProfile


admin.site.site_header = "Talk & Solve Administration"
admin.site.site_title = "Talk & Solve Admin"
admin.site.index_title = "Manage regions, community issues, and users"


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        "community",
        "city",
        "is_active",
    )

    list_filter = (
        "city",
        "is_active",
    )

    search_fields = (
        "city",
        "community",
    )

    ordering = (
        "city",
        "community",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "region",
        "status",
        "created_at",
    )

    list_filter = (
        "category",
        "region",
        "status",
    )

    search_fields = (
        "title",
        "description",
        "city",
        "community",
    )

    fields = (
        "title",
        "description",
        "category",
        "region",
        "city",
        "community",
        "status",
    )

    ordering = (
        "-created_at",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "issue",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "name",
        "message",
        "issue__title",
    )

    ordering = (
        "-created_at",
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "region",
        "city",
        "community",
    )

    list_filter = (
        "region",
        "city",
    )

    search_fields = (
        "user__username",
        "user__email",
        "city",
        "community",
    )