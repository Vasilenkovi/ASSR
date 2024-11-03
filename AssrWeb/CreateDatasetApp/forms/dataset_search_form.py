from CreateDatasetApp.models import DatasetTags
from MetaCommon.forms import SearchForm
from django import forms
class DatasetSearchForm(SearchForm):
    tags1 = DatasetTags.objects.all()
    tags_list = [(i.name, i.name) for i in tags1]
    search_query = forms.CharField(widget=forms.TextInput(attrs={"class": "btn btn-main main-text w-100"}),
                                   required=False, )
    tags = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=tags_list,
    )
    class Meta:
        abstract = False