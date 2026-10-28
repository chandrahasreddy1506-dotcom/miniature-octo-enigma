from django.contrib import admin
from .models import Ward, Community, Issue, Comment, IssueStatusLog


class CommunityInline(admin.TabularInline):
    model = Community
    extra = 1
    fields = ('name', 'postal_code')


class IssueStatusLogInline(admin.TabularInline):
    model = IssueStatusLog
    extra = 0
    readonly_fields = ('changed_by', 'old_status', 'new_status', 'created_at')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('ward_number', 'name', 'zone', 'community_count')
    list_filter = ('zone',)
    search_fields = ('name', 'ward_number', 'zone')
    ordering = ('ward_number',)
    inlines = [CommunityInline]

    def community_count(self, obj):
        return obj.communities.count()
    community_count.short_description = 'Registered Communities'


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward', 'postal_code', 'issue_count')
    list_filter = ('ward__zone', 'ward')
    search_fields = ('name', 'postal_code', 'ward__name')
    ordering = ('name',)

    def issue_count(self, obj):
        return obj.issues.count()
    issue_count.short_description = 'Reported Issues'


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'community', 'get_ward', 'status', 'upvotes', 'author', 'created_at')
    list_filter = ('status', 'category', 'community__ward', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at', 'upvotes')
    inlines = [IssueStatusLogInline]

    def get_ward(self, obj):
        if obj.community and obj.community.ward:
            return f"Ward {obj.community.ward.ward_number}"
        return "-"
    get_ward.short_description = 'Ward'


@admin.register(IssueStatusLog)
class IssueStatusLogAdmin(admin.ModelAdmin):
    list_display = ('issue', 'old_status', 'new_status', 'changed_by', 'created_at')
    list_filter = ('new_status', 'old_status', 'created_at')
    search_fields = ('issue__title', 'changed_by__username')
    readonly_fields = ('issue', 'changed_by', 'old_status', 'new_status', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('issue', 'author', 'created_at', 'short_content')
    search_fields = ('content', 'author__username', 'issue__title')

    def short_content(self, obj):
        return obj.content[:60] + '...' if len(obj.content) > 60 else obj.content
    short_content.short_description = 'Comment'