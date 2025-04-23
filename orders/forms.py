
from django import forms

STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('sent', 'Sent'),
)

class OrderFilterForm(forms.Form):
    loading_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
