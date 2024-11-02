from django import forms


class SearchForm(forms.Form):
    tags = []
    tags_list = [(i.name, i.name) for i in tags]
    search_query = forms.CharField(widget=forms.TextInput(attrs={"class": "btn btn-main main-text w-100"}),required=False,)
    tags =  forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=tags_list,
    )
    class Meta:
        abstract = True