from django import forms
from .models import DataEntry

class DataEntryForm(forms.ModelForm):
    class Meta:
        model = DataEntry
        fields = ['name', 'value']
