from django.contrib import admin
from rest.models import Profile,Comment,Document,Task,Project

# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline
    ]



admin.site.register(Profile)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Comment)
admin.site.register(Document)
admin.site.register(Task)
