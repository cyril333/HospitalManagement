from datetime import date
from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_name', 'dateofbirth', 'age', 'status']
        widgets = {
            'dateofbirth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['age'].required = False
        self.fields['age'].widget.attrs['readonly'] = True

        if self.instance and self.instance.pk:
            self.fields['age'].initial = self.instance.age
        else:
            self.fields['age'].initial = 0

    def clean_age(self):
        dateofbirth = self.cleaned_data.get('dateofbirth')

        if not dateofbirth:
            return 0

        today = date.today()
        age = today.year - dateofbirth.year
        if (today.month, today.day) < (dateofbirth.month, dateofbirth.day):
            age -= 1

        return age

    def clean(self):
        cleaned_data = super().clean()
        dateofbirth = cleaned_data.get('dateofbirth')

        if dateofbirth:
            today = date.today()
            age = today.year - dateofbirth.year
            if (today.month, today.day) < (dateofbirth.month, dateofbirth.day):
                age -= 1
            cleaned_data['age'] = age

        return cleaned_data