from django.forms import ModelForm 
from .models import Product, Image
from django import forms
from tinymce.widgets import TinyMCE


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class CreateProduct(ModelForm):
    name= forms.CharField(label="Nome")
    description=forms.CharField(widget=forms.Textarea(attrs={"rows":5}),label="Descrição")
    price=forms.DecimalField(label="Preço")
   
    highlighted=forms.BooleanField(required=False, label="Destacado")
    new=forms.BooleanField(required=False,label="Novidade")
    # category=forms.HiddenInput()
    main_image=forms.ImageField(label="Imagem Principal")
    detail=forms.CharField(
        label="Detalhes",
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 30}
        )
    )
    class Meta:
        model = Product
        fields = ['name', 'description','price','stock','category','highlighted','new','detail','main_image']
        widgets = {'category': forms.HiddenInput()}

class UpdateImage(ModelForm):
    image=forms.ImageField(label="Imagem Secundária")
    
    class Meta:
        model = Image
        fields = ['image']
        

        

