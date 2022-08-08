from django import forms
from .models import Code

class CodeForm(forms.ModelForm):
    number = forms.CharField(label='Code', help_text='Enter sms verifications')

    class Meta:
        models = Code
        fields = ('number',)
