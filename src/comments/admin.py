from django.contrib import admin

# Register your models here.
from .models import Comment, CommentBlog


class CommentAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'text']
	class Meta:
		model = Comment

admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentBlog)