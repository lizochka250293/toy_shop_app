from django import forms
from django.forms import Textarea

from app_toy_shop.models import Reviews, Star


class ReviewForm(forms.ModelForm):
    description = forms.CharField(label='', widget=Textarea(attrs={'rows': 5}))

    class Meta:
        model = Reviews
        fields = ["description"]


class RatingForm(forms.ModelForm):
    star = forms.ModelChoiceField(
        queryset=Star.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Star
        fields = ('star',)
