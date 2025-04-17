import datetime
from django import forms
from .models import DeliveryNote, PlantTransfer, Package

class DeliveryNoteForm(forms.ModelForm):
    up = forms.ChoiceField(
        choices=[(pt.up, pt.up) for pt in PlantTransfer.objects.all()],
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
        self.user = kwargs.pop('user', None)  # изваждаме user от kwargs
        super().__init__(*args, **kwargs)

        # onchange за UP
        self.fields['up'].widget.attrs.update({
            'onchange': 'updatePlantField(this)'
        })

        # plant readonly
        self.fields['plant'].widget.attrs['readonly'] = True

        # Ако сме в CreateView
        if not self.instance.pk:
            loading = self.get_next_working_day(datetime.date.today())
            self.fields['loading_date'].initial = loading
            self.fields['unloading_date'].initial = loading + datetime.timedelta(days=7)

        # Bootstrap и placeholder-и
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',

            })

        # 👇 Ако потребителят е expeditor
        if self.user.role == 'expeditor':
            for name, field in self.fields.items():
                if name != 'value':
                    field.widget.attrs['readonly'] = True
                    field.disabled = True  # за сигурност и на backend ниво
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

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #
    #     # Set plant на база UP
    #     up = self.cleaned_data.get('up')
    #     pt = PlantTransfer.objects.filter(up=up).first()
    #     if pt:
    #         instance.plant = pt.plant
    #
    #     if commit:
    #         instance.save()
    #     return instance

    def get_next_working_day(self, date):
        next_day = date + datetime.timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += datetime.timedelta(days=1)
        return next_day

