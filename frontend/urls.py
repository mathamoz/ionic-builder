from django.conf.urls import patterns, url

from frontend import views

urlpatterns = patterns('',
	url(r'^list/', views.listing, name='list'),
	url(r'^new', views.new, name='new'),
	url(r'^save', views.save, name='save'),
	# ex: /project/5/
	url(r'^(?P<project_id>\d+)/$', views.detail, name='detail'),
	url(r'^build/(?P<project_id>\d+)/$', views.build, name='build'),
)
