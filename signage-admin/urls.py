from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'reboot', views.reboot, name = 'reboot'),
    url(r'screenshot', views.screenshot, name = 'screenshot'),
    url(r'terminal', views.terminal, name = "terminal"),
    url(r'terminal/resize', views.term_resize, name="term_resize"),
]
