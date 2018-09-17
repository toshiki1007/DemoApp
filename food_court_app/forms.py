from django import forms
from .models import *

class STORE_FORM(forms.ModelForm):
    class Meta:
        model = STORE
        fields = ('store_name', 'start_date', 'image_file')
        
class ORDER_FORM(forms.ModelForm):
    class Meta:
        model = ORDER
        fields = ('__all__')
        
class ORDER_DETAIL_FORM(forms.ModelForm):
    class Meta:
        model = ORDER_DETAIL
        fields = ('__all__')