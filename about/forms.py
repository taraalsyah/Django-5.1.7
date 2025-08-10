from django import forms
from .models import AboutDb

class AboutForm(forms.ModelForm):
    class Meta:
        model=AboutDb
        fields=[
            'nama',
            'alamat',
            'handphone',
            'sex',
        ]