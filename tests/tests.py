from __future__ import absolute_import

from django.test import TestCase, Client, RequestFactory, override_settings

from .models import MyModel, MyUrlModel

from taggit_forms.forms import TagForm
from taggit_forms.utils import create_tag_for_object
from taggit_forms.views import tag_create_view
from taggit_forms.conf import settings


class BaseTestCase(TestCase):
    def setUp(self):
        self.obj = MyModel.objects.create()

    def get_data(self, obj=None):
        obj = obj or self.obj
        return {
            'app_label': obj._meta.app_label,
            'model_name': obj._meta.model_name,
            'object_id': obj.pk,
        }


class FormTest(BaseTestCase):
    def test_form_init(self):
        data = self.get_data()
        form = TagForm(target=self.obj)

        self.assertEqual(form['app_label'].value(), self.obj._meta.app_label)
        self.assertEqual(form['model_name'].value(), self.obj._meta.model_name)
        self.assertEqual(form['object_id'].value(), self.obj.pk)


class UtilTest(BaseTestCase):
    def test_create_tag(self):
        tag_name = 'some tag'
        tags = self.obj.tags.filter(name__exact=tag_name)
        self.assertEqual(len(tags), 0) # tag is not yet created

        create_tag_for_object(tag_name, self.obj)

        tag = self.obj.tags.get(name__exact=tag_name)
        from taggit.models import Tag
        self.assertEqual(tag, Tag.objects.get(name__exact=tag_name)) # tag is created

        create_tag_for_object(tag_name, self.obj)
        tags = self.obj.tags.filter(name__exact=tag_name)
        self.assertEqual(len(tags), 1)


class UrlTest(BaseTestCase):
    urls = 'taggit_forms.urls'
    data = {'tags': 'some tag, another tag'}

    def setUp(self):
        super(UrlTest, self).setUp()
        self.client = Client()

    def test_url(self):
        from django.core.urlresolvers import reverse

        url_name = settings.VIEW_NAME

        url = reverse(url_name)
        data = self.data.copy()
        data.update(self.get_data())

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_named_url(self):
        from django.core.urlresolvers import reverse

        url_name = settings.VIEW_NAME
        kwargs = self.get_data()

        url = reverse(url_name, kwargs=kwargs)
        data = self.data.copy()

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

class ViewTest(BaseTestCase):
    def setUp(self):
        super(ViewTest, self).setUp()
        self.client = Client()
        self.rf = RequestFactory()

    @override_settings(TAGGIT_FORMS={'ALLOWED_METHODS': ['POST'],})
    def test_not_allowed_method(self):
        req = self.rf.get('/')
        res = tag_create_view(req)
        self.assertEqual(res.status_code, 405)

        req = self.rf.put('/')
        res = tag_create_view(req)
        self.assertEqual(res.status_code, 405)

        req = self.rf.delete('/')
        res = tag_create_view(req)
        self.assertEqual(res.status_code, 405)

        req = self.rf.head('/')
        res = tag_create_view(req)
        self.assertEqual(res.status_code, 405)

        # modify allowed method
        with self.settings(TAGGIT_FORMS={'ALLOWED_METHODS': ['PUT'],}):
            req = self.rf.put('/')
            res = tag_create_view(req)
            self.assertNotEqual(res.status_code, 405)

    def test_bad_request(self):
        req = self.rf.post('/')
        res = tag_create_view(req)
        # request without any data is bad
        self.assertEqual(res.status_code, 400)

        data = {'tags': 'some tag, another tag'}
        req = self.rf.post('/', data=data)
        res = tag_create_view(req)
        # request without app_label or model_name or object_id is bad
        self.assertEqual(res.status_code, 400)

        data = {'tags': 'some tag', 'app_label': 'bar', 'model_name': 'foo', 'object_id': 1}
        req = self.rf.post('/', data=data)
        res = tag_create_view(req)
        # request with no existing app_label and model_name is bad
        self.assertEqual(res.status_code, 400)

        data = {'tags': 'some tag, another tag'}
        data.update(self.get_data())
        data['object_id'] = -1 # non-existing pk
        req = self.rf.post('/', data=data)
        res = tag_create_view(req)
        # request with no existing app_label and model_name is bad
        self.assertEqual(res.status_code, 400)

    def test_nice_request(self):
        tags = ['some tag', 'another tag']
        data = {'tags': ','.join(tags)}
        data.update(self.get_data())
        req = self.rf.post('/', data=data)
        res = tag_create_view(req)
        self.assertEqual(res.status_code, 302)

        for tag_name in tags:
            self.assertTrue(self.obj.tags.filter(name__exact=tag_name))

    def test_success_url(self):
        from django.core.urlresolvers import reverse

        def assert_redirect_url(expected_url):
            data = {'tags': 'some tag, another tag'}
            data.update(self.get_data())
            req = self.rf.post('/', data=data)
            res = tag_create_view(req)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.url, expected_url)

        # simple fixed success url setting
        with self.settings(TAGGIT_FORMS={'SUCCESS_URL': '/somewhere',}):
            assert_redirect_url('/somewhere')

        # callable success url
        with self.settings(TAGGIT_FORMS={'SUCCESS_URL': lambda obj, request: '/elsewhere',}):
            assert_redirect_url('/elsewhere')

        # without SUCCESS_URL setting
        with self.settings(TAGGIT_FORMS={'SUCCESS_URL': None,}):
            # redirect to root URL
            assert_redirect_url('/')

            # if model has get_absolute_url method, redirect to there
            obj = MyUrlModel.objects.create()
            expected_url = obj.get_absolute_url()
            data = {'tags': 'some tag, another tag'}
            data.update(self.get_data(obj))
            req = self.rf.post('/', data=data)
            res = tag_create_view(req)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.url, expected_url)


class ConfTest(TestCase):
    @override_settings(TAGGIT_FORMS={
            'URL_NAMESPACE': 'some_namespace',
            'SUCCESS_URL': 'some_url',
            'ALLOWED_METHODS': ['POST', 'PUT'],
        })
    def test_conf(self):
        self.assertEqual(settings.URL_NAMESPACE, 'some_namespace')
        self.assertEqual(settings.SUCCESS_URL, 'some_url')
        self.assertEqual(settings.ALLOWED_METHODS, ['POST', 'PUT'])

        with self.assertRaises(AttributeError):
            settings.BAR_FOO


class TemplateTagTest(BaseTestCase):
    @override_settings(TAGGIT_FORMS={'URL_NAMESPACE': 'taggit_forms',})
    def test_render_tag(self):
        from django.template import Template, Context

        template = Template('{% load taggitforms %} {% render_tag_form obj %}')
        context = Context({'obj': self.obj})
        rendered = template.render(context)
        html = '''<form method="post" action="/taggit_forms/">
                    <input id="id_tags" name="tags" type="text" />
                    <input id="id_app_label" name="app_label" type="hidden" value="tests" />
                    <input id="id_model_name" name="model_name" type="hidden" value="mymodel" />
                    <input id="id_object_id" name="object_id" type="hidden" value="1" />
                    <button type="submit">Submit</button>
                </form>'''
        self.assertHTMLEqual(html, rendered)

    def test_get_tag(self):
        from django.template import Template, Context

        template = Template('''{% load taggitforms %}
            {% get_tag_form obj as tag_form %}
            {% for field in tag_form %}
              {{ field }}
            {% endfor %}
            ''')
        context = Context({'obj': self.obj})
        rendered = template.render(context)
        html = '''<input id="id_tags" name="tags" type="text" />
                    <input id="id_app_label" name="app_label" type="hidden" value="tests" />
                    <input id="id_model_name" name="model_name" type="hidden" value="mymodel" />
                    <input id="id_object_id" name="object_id" type="hidden" value="1" />'''
        self.assertHTMLEqual(html, rendered)

