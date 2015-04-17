from django import template
from django.core.urlresolvers import reverse

from taggit_forms.conf import settings
from taggit_forms.forms import TagForm

register = template.Library()


@register.inclusion_tag(settings.TEMPLATE_NAME)
def render_tag_form(obj):
    form = TagForm(target=obj)

    url = reverse(':'.join([settings.URL_NAMESPACE, settings.VIEW_NAME]))
    return {'form': form, 'url': url}


@register.assignment_tag
def get_tag_form(obj):
    form = TagForm(target=obj)
    return form
