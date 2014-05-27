from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from frontend import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'builder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^projects/', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^how-it-works/', views.howitworks, name='howitworks'),
    url(r'^project/new', views.new, name='new'),
    url(r'^project/save', views.save, name='save'),
    url(r'^admin/', include(admin.site.urls)),
)
