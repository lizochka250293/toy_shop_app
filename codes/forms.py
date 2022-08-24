from django import forms

from .models import Code


class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Код', help_text='Введите код')

    class Meta:
        model = Code
        fields = ('number',)
