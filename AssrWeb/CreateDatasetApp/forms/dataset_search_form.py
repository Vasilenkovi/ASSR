from CreateDatasetApp.models import DatasetMetadata
from django import forms
class DatasetSearchForm(forms.ModelForm):
    search_query = forms.CharField(widget=forms.TextInput(attrs={"class": "btn btn-main main-text w-100"}),
                                   required=False, )
    class Meta:
        model = DatasetMetadata
        fields = ["tag"]
        widgets = {"tag": forms.CheckboxSelectMultiple}
        abstract = False