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
    ORDER_QTY = (
        (0,0),
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5),
        (6,6),
        (7,7),
        (8,8),
        (9,9)
        )
    
    order_qty = forms.ChoiceField(choices=ORDER_QTY, widget=forms.Select())
    class Meta:
        model = ORDER_DETAIL
        fields = ('__all__')