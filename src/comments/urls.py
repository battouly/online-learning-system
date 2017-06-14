from django.conf.urls import patterns, include,url
from django.contrib import admin

# from .views import (
#     comment_thread_Blog,
#     comment_delete_Blog

#     )

urlpatterns = patterns('comments.views',

    url(r'^(?P<id>\d+)/$', 'comment_thread_Blog', name='thread'),
    url(r'^(?P<id>\d+)/delete/$', 'comment_delete_Blog', name='delete'),
	)


