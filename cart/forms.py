from django import forms
from django.forms.utils import ErrorList

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Колличество', choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(
            self,
            data=None,
            files=None,
            auto_id="id_%s",
            prefix=None,
            initial=None,
            error_class=ErrorList,
            label_suffix=None,
            empty_permitted=False,
            field_order=None,
            use_required_attribute=None,
            renderer=None,
            count=None
    ):
        super().__init__(
            data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
            use_required_attribute, renderer
        )
        if count is not None:
            self.fields['quantity'].choices = [(i, str(i)) for i in range(1, count+1)]
