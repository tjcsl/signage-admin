"""signage_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, { 'template_name' : 'login.html' , 'redirect_field_name' : 'next' }, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/login/$', RedirectView.as_view(url="/login?next=/", permanent=False), name='index'),
    url(r'^accounts/logout/$', RedirectView.as_view(url="/logout", permanent=False), name='index'),
    url(r'^favicon.ico$', RedirectView.as_view(url="/static/monitor.svg", permanent=False), name='index'),
    url(r'^', include('signage-admin.urls'), name = 'index'),
    #url(r'^$', RedirectView.as_view(url="/signage-adman", permanent=False), name='index'),
]
