import datetime
from django import forms
from .models import DeliveryNote, PlantTransfer, Package


class DeliveryNoteForm(forms.ModelForm):
    up = forms.ChoiceField(
        choices=[('', 'Select UP')] + [(pt.up, pt.up) for pt in PlantTransfer.objects.all()],
        label='UP',
        required=True
    )
    package_type = forms.ModelChoiceField(
        queryset=Package.objects.all(),
        label="Package Type",
        required=True
    )

    class Meta:
        model = DeliveryNote
        fields = [
            'delivery_note_number',
            'up',
            'plant',
            'loading_date',
            'unloading_date',
            'package_type',
            'package_count',
            'total_height',
            'total_weight',
            'value',
        ]

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if not self.instance.pk:
            loading = self.get_next_working_day(datetime.date.today())
            self.fields['loading_date'].initial = loading
            self.fields['unloading_date'].initial = loading + datetime.timedelta(days=7)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['total_height'].widget.attrs['placeholder'] = 'in M'
        self.fields['total_weight'].widget.attrs['placeholder'] = 'in KG'

        # 🔐 Контрол по order.status
        order = getattr(self.instance, 'order', None)
        order_status = getattr(order, 'status', None)

        if order_status == 1:
            # Цялата форма е само за четене
            for field in self.fields.values():
                field.disabled = True
                field.widget.attrs['readonly'] = True

        elif order_status == 0:
            # Само value се редактира
            for name, field in self.fields.items():
                if name != 'value':
                    field.disabled = True
                    field.widget.attrs['readonly'] = True


        elif not order:
            if self.user.role == 'expeditor':
                for name, field in self.fields.items():
                    if name != 'value':
                        field.widget.attrs['readonly'] = True
                        field.disabled = True
            elif self.user.role == 'dispatcher':
                self.fields.pop('value', None)

    def clean_delivery_note_number(self):
        number = self.cleaned_data['delivery_note_number']
        if len(str(number)) != 8:
            raise forms.ValidationError("Delivery Note Number must be exactly 8 digits.")
        return number

    def clean(self):
        cleaned_data = super().clean()
        numeric_fields = ['package_count', 'total_height', 'total_weight', 'value']
        for field in numeric_fields:
            val = cleaned_data.get(field)
            if val is not None and val < 0:
                self.add_error(field, 'This field cannot be negative.')

    def get_next_working_day(self, date):
        next_day = date + datetime.timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += datetime.timedelta(days=1)
        return next_day
