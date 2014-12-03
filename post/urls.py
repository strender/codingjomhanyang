from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studyplan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^(?P<challenge_id>\d+)/create/$', views.create_post, name='create_post'),
    url(r'^(?P<challenge_id>\d+)/(?P<post_id>\d+)/edit/$', views.edit_post, name='edit_post'),
    url(r'^(?P<challenge_id>\d+)/(?P<post_id>\d+)/delete/$', views.delete_post, name='delete_post'),
    url(r'^(?P<challenge_id>\d+)/(?P<post_id>\d+)/like/$', views.like_post, name='like_post'),
    url(r'^(?P<challenge_id>\d+)/(?P<post_id>\d+)/comment/$', views.create_comment, name='create_comment'),
    url(r'^(?P<challenge_id>\d+)/(?P<post_id>\d+)/comment/(?P<comment_id>\d+)/delete/$', views.delete_comment, name='delete_comment'),

    url(r'^(?P<challenge_id>\d+)/view/(?P<post_id>\d+)$', views.view_post, name='view_post'),

)
