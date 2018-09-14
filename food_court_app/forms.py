from django import forms
from .models import *

class STORE_FORM(forms.ModelForm):
    class Meta:
        model = STORE
        fields = ('store_name', 'start_date', 'image_file')