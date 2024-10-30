from django import forms
from CreateDatasetApp.models import DatasetMetadata
from MetaCommon.forms.widgets.key_value_widget import KeyValueWidget


class DatasetMetadataForm(forms.ModelForm):
    class Meta:
        model = DatasetMetadata
        fields = ["name", "author", "keyValue", "tag"]
        widgets = {
            "keyValue": KeyValueWidget,
            "tag": forms.CheckboxSelectMultiple
        }