from django.forms import ModelForm, HiddenInput, CharField
from MetaCommon.forms.widgets.key_value_widget import KeyValueWidget
from ProcessingApp.models import Processing_model


class Processing_Form(ModelForm):
    parameters_kv = CharField(widget=KeyValueWidget(), required=False)

    class Meta:
        model = Processing_model
        fields = ('dataset', 'model', 'parameters')
        widgets = {
            'parameters': HiddenInput()
        }

    def clean(self):
        return super().clean()

    def clean_parameters(self):
        data: dict = self.cleaned_data['parameters']
        
        return {k.strip(): v.strip() for k, v in data.items()}
    
    def clean_model(self):
        data: str = self.cleaned_data['model']
        
        return data.strip()
