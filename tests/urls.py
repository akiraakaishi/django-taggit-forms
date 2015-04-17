from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^taggit_forms/', include('taggit_forms.urls', namespace='taggit_forms')),
)
