from django import forms
from CreateDatasetApp.models import DatasetTags
from MetaCommon.forms import SearchForm
class DatasetSearchForm(SearchForm):
    tags = DatasetTags.objects.all()
    class Meta:
        abstract = False