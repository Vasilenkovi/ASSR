from django import forms
from UploadSource.models.source_file_meta import SourceMetadata, SourceTags
from MetaCommon.forms.widgets.key_value_widget import KeyValueWidget


class SourceMetadataForm(forms.ModelForm):
    class Meta:
        model = SourceMetadata
        fields = ["name", "author", "keyValue", "tag"]
        widgets = {
            "keyValue": KeyValueWidget
        }