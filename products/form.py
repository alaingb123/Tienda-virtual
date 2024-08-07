from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductImage


input_css_class = "form-control"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','clasificacion', 'handle', 'price', 'supply']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", 'name','clasificacion', 'handle', 'price', 'supply']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = input_css_class



class ProductAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ["file", 'name', 'is_free', 'active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            if field in ['is_free', 'active']:
                continue
            self.fields[field].widget.attrs['class'] = input_css_class


ProductAttachmentModelFormSet = modelformset_factory(
    ProductImage,
    form=ProductAttachmentForm,
    fields = ['file', 'name','is_free', 'active'],
    extra=0,
    can_delete=True
)

ProductAttachmentInlineFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form = ProductAttachmentForm,
    formset = ProductAttachmentModelFormSet,
    fields = ['file', 'name','is_free', 'active'],
    extra=0,
    can_delete=True
)