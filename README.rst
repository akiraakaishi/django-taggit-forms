=============
django-taggit-forms
=============

.. image:: https://travis-ci.org/akiraakaishi/django-taggit-forms.svg?branch=master
    :target: https://travis-ci.org/akiraakaishi/django-taggit-forms

.. image:: https://coveralls.io/repos/akiraakaishi/django-taggit-forms/badge.svg?branch=master
  :target: https://coveralls.io/r/akiraakaishi/django-taggit-forms?branch=master

.. image:: https://codeclimate.com/github/akiraakaishi/django-taggit-forms/badges/gpa.svg
  :target: https://codeclimate.com/github/akiraakaishi/django-taggit-forms/badges/gpa.svg


``django-taggit-forms`` handles form submissions to create a tag by use of the ``django-taggit`` package.

Usage
======

Add ``'taggit_forms'`` to your ``INSTALLED_APPS``.
(Make sure that ``taggit`` and ``django.contrib.contenttypes`` are also included in ``INSTALLED_APPS``.)
In your root ``urls.py``, include ``'taggit_forms.urls'`` with the namespace ``'taggit_forms'``.

.. code:: python

    urlpatterns = patterns('',
        # your urls
    
        url(r'^taggit_forms/', include('taggit_forms.urls', namespace='taggit_forms')),
    )

Then, create your model to be tagged with:

.. code:: python

    class MyModel(models.Model):
       tags = TaggableManager()

Then, in your templates, render a tag-creation form for an instance of ``MyModel`` with the template tag ``render_tag_form``::

    {% load taggitforms%}
    {% render_tag_form my_obj %}

The form is rendered with the template ``taggit_forms/form.html``.

Altenatively, use the template tag ``get_tag_form`` to assign the form as a context variable::

    {% get_tag_form my_obj as tag_form %}
    {% for field in tag_form %}
        {{ field }}
    {% endfor %}
