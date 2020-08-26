from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView, LogoutView
from simplemooc.accounts import views
from django.conf import settings
from simplemooc import urls

urlpatterns = [
    #re_path(r'^(?P<pk>\d+)$', views.details, name='details'),
    re_path(r'^entrar/$', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    re_path(r'^sair/$', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    re_path(r'^cadastre-se/$', views.register, name='register'),
    re_path(r'^editar/$', views.edit, name='edit'),
    re_path(r'^editar-senha/$', views.edit_password, name='edit_password'),
    re_path(r'^nova-senha/$', views.password_reset, name='password_reset'),
    re_path(r'^confirmar-nova-senha/(?P<key>\w+)/$', views.password_reset_confirm, name='password_reset_confirm'),
    re_path(r'^$', views.dashboard, name='dashboard'),
]
