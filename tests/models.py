from django.db import models

from taggit.managers import TaggableManager

class MyModel(models.Model):
    tags = TaggableManager()

class MyUrlModel(MyModel):
    def get_absolute_url(self):
        return '/model-page'
