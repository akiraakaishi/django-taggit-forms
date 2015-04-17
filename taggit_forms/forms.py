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

    _obj = None

    def __init__(self, *args, **kwargs):
        target = kwargs.pop('target', None)
        if target is not None:
            initial = kwargs.get('initial', {})
            initial['app_label'] = target._meta.app_label
            initial['model_name'] = target._meta.model_name
            initial['object_id'] = target.pk
            kwargs['initial'] = initial
        super(TagForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(TagForm, self).clean()

        app_label = cleaned_data.get('app_label')
        model_name = cleaned_data.get('model_name')
        object_id = cleaned_data.get('object_id')
        if not (app_label and model_name and object_id):
            raise ValidationError('unable to specify the object.')

        try:
            Model = get_model(app_label, model_name)
        except LookupError as e:
            raise ValidationError(e)

        try:
            obj = Model._default_manager.get(pk=object_id)
        except Model.DoesNotExist:
            raise ValidationError('object does not exist')

        self._obj = obj

        return cleaned_data
