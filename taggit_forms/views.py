from django import http

from taggit_forms.forms import TagForm
from taggit_forms.utils import create_tag_for_object
from taggit_forms.conf import settings


def tag_create_view(request, *args, **kwargs):
    if request.method not in settings.ALLOWED_METHODS:
        return http.HttpResponseNotAllowed(settings.ALLOWED_METHODS)

    for key in ['app_label', 'model_name', 'object_id']:
        if key in kwargs:
            request.POST[key] = kwargs[key]

    form = TagForm(data=request.POST)
    if not form.is_valid():
        return http.HttpResponseBadRequest()

    obj = form._obj
    assert obj

    tags = form.cleaned_data['tags']
    for tag_name in tags:
        create_tag_for_object(tag_name, obj)

    if settings.SUCCESS_URL:
        if callable(settings.SUCCESS_URL):
            success_url = settings.SUCCESS_URL(obj, request)
        else:
            success_url = settings.SUCCESS_URL
    elif hasattr(obj, 'get_absolute_url'):
        success_url = obj.get_absolute_url()
    else:
        success_url = '/'

    return http.HttpResponseRedirect(success_url)
