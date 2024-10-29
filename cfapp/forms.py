from django import forms
from .models import Incasso, Transazione


class TransazioneForm(forms.ModelForm):
    incassi = forms.ModelMultipleChoiceField(
        queryset=Incasso.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Transazione
        fields = ["tipologia", "data", "importo", "incassi"]

    def save(self, commit=True):
        transazione = super().save(commit=commit)
        if commit:
            transazione.incassi.set(self.cleaned_data["incassi"])
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
