from django import forms
from .models import PlantTransfer


class PlantTransferForm(forms.ModelForm):
    class Meta:
        model = PlantTransfer
        fields = ['up', 'plant']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
