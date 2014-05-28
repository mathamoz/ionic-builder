from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from frontend import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'builder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^projects/', include('frontend.urls')),
    url(r'^project/', include('frontend.urls')),
    url(r'^about/', views.about, name='about'),
    url(r'^how-it-works/', views.howitworks, name='howitworks'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^updates/builder', views.builder, name='builder'),
)
