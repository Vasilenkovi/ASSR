from UploadSource.models import SourceMetadata
from django import forms


class SourceSearchForm(forms.ModelForm):
    search_query = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "btn btn-main main-text w-100"}
        ),
        required=False,
    )

    class Meta:
        model = SourceMetadata
        fields = ["tag"]
        widgets = {"tag": forms.CheckboxSelectMultiple}
        abstract = False
