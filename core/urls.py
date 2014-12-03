from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'studyplan.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'core.views.index', name='index'),
    url(r'^home/(?P<challenge_id>\d+)/$', 'core.views.home', name='home'),
)
