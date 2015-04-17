from django.conf.urls import patterns, url

from taggit_forms.views import tag_create_view
from taggit_forms.conf import settings

urlpatterns = patterns('',
    url(r'^$', tag_create_view, name=settings.VIEW_NAME),
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/(?P<object_id>\d+)$', tag_create_view, name=settings.VIEW_NAME),
)
