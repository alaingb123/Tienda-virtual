from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Product, ProductImage


input_css_class = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
select_css_class = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 appearance-none"



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'clasificaciones_padre','clasificacion', 'handle', 'price', 'supply', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['placeholder'] = "Your name"
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = select_css_class


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["image", 'name', 'keywords','clasificaciones_padre', 'clasificacion', 'handle', 'price', 'supply', 'description','active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field].widget, forms.Select):
                self.fields[field].widget.attrs['class'] = select_css_class
            else:
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
            self.fields[field].widget.attrs['class'] = select_css_class


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
