from django.contrib import admin

from rest.models import (
    Comment,
    CustomUser,
    Document,
    Notification,
    Profile,
    Project,
    Task,
    Timeline,
)


class CommentInline(admin.TabularInline):
    model = Comment


class ProjectAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

    list_display = (
        "title",
        "manager",
    )


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
    )


admin.site.register(CustomUser)
admin.site.register(Profile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment)
admin.site.register(Document)
admin.site.register(Task, TaskAdmin)
admin.site.register(Notification)
admin.site.register(Timeline)
