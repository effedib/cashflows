from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Transazione, Incasso


class TransazioneForm(forms.ModelForm):
    incassi = forms.ModelMultipleChoiceField(
        queryset=Incasso.objects.all(),
        required=False,
        # widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Transazione
        fields = ["importo", "tipologia", "data", "incassi"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Row(
                Column("importo", css_class="form-group col-md-6 mb-0"),
                Column("tipologia", css_class="form-group col-md-6 mb-0"),
                css_class="form-row",
            ),
            "data",
            "incassi",
            Submit("submit", "Salva"),
        )
