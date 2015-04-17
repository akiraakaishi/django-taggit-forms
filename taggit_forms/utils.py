from django.contrib.contenttypes.models import ContentType

from taggit.models import Tag, TaggedItem


def create_tag_for_object(tag_name, obj):
    tag, tag_created = Tag.objects.get_or_create(name=tag_name)
    content_type = ContentType.objects.get_for_model(obj._meta.model)

    tagged_item, tagged_item_created = TaggedItem.objects.get_or_create(tag=tag, content_type=content_type, object_id=obj.pk)
