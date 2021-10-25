from django.forms import ModelForm 
from .models import Cupon


class CreateCupon(ModelForm):
    class Meta:
        model=Cupon
        exclude=('is_active',)