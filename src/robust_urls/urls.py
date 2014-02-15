from django.conf.urls import patterns, url

from .views import set_language


urlpatterns = patterns('',
    url(r'^setlang/$', set_language, name='set_language'),
)