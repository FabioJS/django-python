from django.contrib import admin
from django.urls import path, include, re_path
from simplemooc.courses import views
from simplemooc import urls

urlpatterns = [
    #re_path(r'^(?P<pk>\d+)$', views.details, name='details'),
    re_path(r'(?P<slug>[\w_-]+)$', views.details, name='details'),
    re_path(r'(?P<slug>[\w_-]+)/inscricao/$', views.enrollment, name='enrollment'),
    re_path(r'(?P<slug>[\w_-]+)/anuncios/$', views.announcements, name='announcements'),
    re_path(r'(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', views.show_announcement, name='show_announcement'),
    re_path(r'(?P<slug>[\w_-]+)/cancelar-inscricao/$', views.undo_enrollment, name='undo_enrollment'),
    re_path(r'^$', views.index, name='index'),
]
