from django.forms.widgets import Widget

class KeyValueWidget(Widget):
    template_name = "widgets/table_keys.html"