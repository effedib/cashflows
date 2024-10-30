from django import forms
from .models import Incasso, Transazione


class TransazioneForm(forms.ModelForm):
    class Meta:
        model = Transazione
        fields = ["importo", "tipologia", "data", "incassi"]

    incassi = forms.ModelMultipleChoiceField(
        queryset=Incasso.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def save(self, commit=True):
        transazione = super().save(commit=commit)
        if commit:
            incassi = self.cleaned_data["incassi"]
            # transazione.importo = sum(incasso.importo for incasso in incassi)
            transazione.incassi.set(incassi)
            transazione.save()
        return transazione


class IncassoForm(forms.ModelForm):
    transazioni = forms.ModelMultipleChoiceField(
        queryset=Transazione.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Incasso
        fields = "__all__"
