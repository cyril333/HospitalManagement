from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import DoctorProfile, NurseProfile, UserProfile


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = f'{existing} form-select'.strip()
            else:
                field.widget.attrs['class'] = f'{existing} form-control'.strip()


class DoctorForm(StyledModelForm):
    SPECIALIZATION_CHOICES = [
        ('', 'Select Specialization'),
        ('General Medicine', 'General Medicine'),
        ('Pediatrics', 'Pediatrics'),
        ('Cardiology', 'Cardiology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Dermatology', 'Dermatology'),
        ('Obstetrics and Gynecology', 'Obstetrics and Gynecology'),
        ('Surgery', 'Surgery'),
        ('Radiology', 'Radiology'),
        ('Anesthesiology', 'Anesthesiology'),
    ]

    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    specialization = forms.ChoiceField(
        choices=SPECIALIZATION_CHOICES,
        widget=forms.Select()
    )

    class Meta:
        model = DoctorProfile
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'department',
            'specialization',
            'license_number',
            'contact_number',
            'daily_rate',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Leave blank to keep the current password.'

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        qs = User.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError('This username is already taken.')
        return username

    def clean_daily_rate(self):
        daily_rate = self.cleaned_data.get('daily_rate')
        if daily_rate is not None and daily_rate < 0:
            raise ValidationError('Daily rate cannot be negative.')
        return daily_rate

    def save(self, commit=True, created_by_admin=None):
        if self.instance and self.instance.pk:
            user = self.instance.user
            user.first_name = self.cleaned_data['first_name'].strip()
            user.last_name = self.cleaned_data['last_name'].strip()
            user.username = self.cleaned_data['username'].strip()
            user.email = self.cleaned_data['email'].strip()

            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
            if commit:
                user.save()

            doctor = super().save(commit=False)
            doctor.user = user
            if commit:
                doctor.save()
            return doctor

        user = User(
            first_name=self.cleaned_data['first_name'].strip(),
            last_name=self.cleaned_data['last_name'].strip(),
            username=self.cleaned_data['username'].strip(),
            email=self.cleaned_data['email'].strip(),
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        if commit:
            UserProfile.objects.create(
                user=user,
                role='Doctor',
                created_by_admin=created_by_admin
            )

        doctor = super().save(commit=False)
        doctor.user = user
        if commit:
            doctor.save()
        return doctor


class NurseForm(StyledModelForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = NurseProfile
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'department',
            'shift_schedule',
            'contact_number',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['password'].required = False
            self.fields['password'].help_text = 'Leave blank to keep the current password.'

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        qs = User.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.user.pk)
        if qs.exists():
            raise ValidationError('This username is already taken.')
        return username

    def save(self, commit=True, created_by_admin=None):
        if self.instance and self.instance.pk:
            user = self.instance.user
            user.first_name = self.cleaned_data['first_name'].strip()
            user.last_name = self.cleaned_data['last_name'].strip()
            user.username = self.cleaned_data['username'].strip()
            user.email = self.cleaned_data['email'].strip()

            password = self.cleaned_data.get('password')
            if password:
                user.set_password(password)
            if commit:
                user.save()

            nurse = super().save(commit=False)
            nurse.user = user
            if commit:
                nurse.save()
            return nurse

        user = User(
            first_name=self.cleaned_data['first_name'].strip(),
            last_name=self.cleaned_data['last_name'].strip(),
            username=self.cleaned_data['username'].strip(),
            email=self.cleaned_data['email'].strip(),
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        if commit:
            UserProfile.objects.create(
                user=user,
                role='Nurse',
                created_by_admin=created_by_admin
            )

        nurse = super().save(commit=False)
        nurse.user = user
        if commit:
            nurse.save()
        return nurse