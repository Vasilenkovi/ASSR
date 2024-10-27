from django.db import IntegrityError
from .consumer import AbstractConsumer
from MetaCommon.models import Tags


class TagConsumer(AbstractConsumer):
    tag_class: Tags = None

    def _tag_object_factory(self, tag_name: str) -> Tags | None:
       return self.tag_class.objects.create(name=tag_name)

    def handlerTagAddition(self, tagName: str):

        try:
            tag = self._tag_object_factory(tagName)
            response = {
                "success": True,
                "id": tag.pk,
                "name": tag.name
            }
            self.sendResponse(response)

        except IntegrityError:
            response = {
                "success": False,
                "reason": "tag exists"
            }
            self.sendResponse(response)

    # No reason for it to be here. Single responsibility principle
    def handlerColumnsDrop(self, columnsList, fileList):
        pass