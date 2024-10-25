from django.test import TestCase
from django.db import IntegrityError
from UploadSource.models import SourceTags


class TestsSourceTags(TestCase):

    def test_blank(self):
        with self.assertRaises(IntegrityError):
            SourceTags.objects.create(name=None)

    def test_unique(self):
        tag = SourceTags.objects.create(name="tag_name_1")
        self.assertTrue(tag.pk)

        with self.assertRaises(IntegrityError):
            SourceTags.objects.create(name="tag_name_1")
