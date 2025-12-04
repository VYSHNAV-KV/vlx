from django import forms
from .models import productdb, categorydb

class ProductDBForm(forms.ModelForm):
    class Meta:
        model = productdb
        fields = [
            'Categoryname', 'Subcategoryname', 'Productname', 'Ownername',
            'Price', 'Mobile', 'Location','Description',
            'Vehicleimage1', 'Vehicleimage2', 'Vehicleimage3', 'AdditionalData'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            category = kwargs['instance'].Categoryname
            self.adjust_fields_based_on_category(category)

    def adjust_fields_based_on_category(self, category):
        if category == "Cars":
            self.fields['AdditionalData'].widget = forms.Textarea(attrs={
                'placeholder': 'Enter car-specific details like fuel type, mileage, etc.'
            })
        elif category == "Bikes":
            self.fields['AdditionalData'].widget = forms.Textarea(attrs={
                'placeholder': 'Enter bike-specific details like engine type, cc, etc.'
            })
        else:
            self.fields['AdditionalData'].widget = forms.Textarea(attrs={
                'placeholder': 'Enter other product details'
            })
