from django import forms
from UploadSource.models.source_file_meta import SourceMetadata, SourceTags
from MetaCommon.forms.widgets.key_value_widget import KeyValueWidget
from MetaCommon.forms import _get_options


def _get_source_options():
    return _get_options(SourceTags.objects.all())


class SourceMetadataForm(forms.ModelForm):

    #tag = forms.ChoiceField(choices=_get_source_options, 
    #                        widget=forms.CheckboxSelectMultiple
    #                        )

    class Meta:
        model = SourceMetadata
        fields = ["name", "author", "keyValue", "tag"]
        widgets = {
            "keyValue": KeyValueWidget,
            "tag": forms.CheckboxSelectMultiple
        }