from django.db.models import fields
from django.forms import ModelForm 
from orders.models import Order, Shipment
from django import forms


class UpdateOrder1(ModelForm):

    payment_receipt=forms.FileField(required=False, label="Comprovativo de Pagamento")
    

    class Meta:
        model = Order
        fields = ['payment_receipt' ,'state']
        widgets = {'state': forms.HiddenInput()}

class UpdateOrder2(ModelForm):
    

    class Meta:
        model = Order
        fields = ['state' ]
        widgets = {'state': forms.HiddenInput()}

class UpdateOrder3(ModelForm):
    tracking_number=forms.CharField(required=False)
    invoice=forms.FileField(required=False, label="Fatura")

    class Meta:
        model = Order
        fields = ['tracking_number', 'invoice','state' ]
        widgets = {'state': forms.HiddenInput()}

class ShipmentForm(ModelForm):
    name=forms.CharField(label="Nome")
    price=forms.CharField(label="Preço")

    class Meta:
        model= Shipment
        fields = '__all__'