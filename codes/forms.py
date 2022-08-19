from django import forms

from .models import Code


class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Код', help_text='Отравьте для аутефикации')

    class Meta:
        model = Code
        fields = ('number',)
