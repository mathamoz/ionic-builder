from django.conf.urls import patterns, url

from frontend import views

urlpatterns = patterns('',
    url(r'^list/', views.listing, name='list'),
    url(r'^updates/builder', views.builder, name='builder'),
    url(r'^new', views.new, name='new'),
    url(r'^save', views.save, name='save'),
)
