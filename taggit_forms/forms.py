from django import forms
from django.core.exceptions import ValidationError

from taggit.forms import TagField


try:
    from django.apps.apps import get_model
except ImportError:
    from django.db.models import get_model


class TagForm(forms.Form):
    tags = TagField()

    app_label = forms.CharField(required=True, widget=forms.HiddenInput())
    model_name = forms.CharField(required=True, widget=forms.HiddenInput())
    object_id = forms.CharField(required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        target = kwargs.pop('target', None)
        if target is not None:
            initial = kwargs.get('initial', {})
            initial['app_label'] = target._meta.app_label
            initial['model_name'] = target._meta.model_name
            initial['object_id'] = target.pk
            kwargs['initial'] = initial
        super(TagForm, self).__init__(*args, **kwargs)

    _obj = None
    def clean(self):
        cleaned_data = super(TagForm, self).clean()

        try:
            Model = get_model(cleaned_data['app_label'], cleaned_data['model_name'])
        except LookupError as e:
            raise ValidationError(e.message)

        try:
            obj = Model._default_manager.get(pk=cleaned_data['object_id'])
        except Model.DoesNotExist:
            raise ValidationError('object does not exist')

        self._obj = obj

        return cleaned_data
