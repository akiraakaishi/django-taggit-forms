from django.conf import settings as django_settings

try:
    from django.core.signals import setting_changed
except ImportError:
    from django.test.signals import setting_changed

TAGGIT_FORMS = {
    'URL_NAMESPACE': 'taggit_forms',
    'VIEW_NAME': 'submit_tag',
    'SUCCESS_URL': None,
    'ALLOWED_METHODS': ['POST'],
    'TEMPLATE_NAME': 'taggit_forms/form.html',
}


class Settings(object):
    FIXED_SETTINGS = ('VIEW_NAME', )

    def __init__(self, default):
        setattr(self, 'default', default)
        user_settings = getattr(django_settings, 'TAGGIT_FORMS', {})
        self._update(user_settings)

    def _update(self, user_settings):
        for key in self.default:
            if key in user_settings and key not in self.FIXED_SETTINGS:
                self.default[key] = user_settings[key]

    def __getattr__(self, name):
        if name in self.default:
            return self.default[name]
        raise AttributeError

settings = Settings(TAGGIT_FORMS)


def update_settings(*args, **kwargs):
    if kwargs['setting'] == 'TAGGIT_FORMS':
        value = kwargs['value']
        if value:
            settings._update(value)

setting_changed.connect(update_settings)
