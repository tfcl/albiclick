
from store.models import Cart
from users.models import Adress
from django.db import models
from django.contrib.auth.models import User

class Cupon(models.Model):
    code=models.CharField(max_length=120)
    is_free_shipping=models.BooleanField()
    discount=models.IntegerField()
    max_redeem=models.IntegerField()
    is_active=models.BooleanField(default=True)
    

class Shipment(models.Model):
    name= models.CharField(max_length=120) 
    price=models.DecimalField(max_digits=6, decimal_places=2)
    


class Payment(models.Model):
    #dados duplicados, é melhor criar um fk co tipo de pagamento
    name= models.CharField(max_length=120) 
    
    # def get_details(self):
    #     details=self.objects.filter(pk=self.pk)
    #     return details

class Detail(models.Model):
    payment=models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    title=models.CharField(max_length=120) 
    description=models.CharField(max_length=120) 
   

class Order(models.Model):
    STATES=(
        ('0','Cancelada'),
        ('1','A Aguardar Pagamento'),
        ('2','Pagamento Confirmado'),
        ('3','Em Processamento'),
        ('4','Enviado'),

    )

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.DO_NOTHING, null=True)
    adress=models.ForeignKey(Adress,related_name="order_adress", on_delete=models.CASCADE) 
    adress_billing=models.ForeignKey(Adress,related_name="order_adress_billing", on_delete=models.CASCADE, null=True, blank=True) 
    payment=models.OneToOneField(Payment,related_name="payment", on_delete=models.CASCADE,null=True)

    cupon=models.ForeignKey(Cupon,on_delete=models.DO_NOTHING, null=True)
    shipment=models.ForeignKey(Shipment, on_delete=models.CASCADE, null=True) 
    total=models.DecimalField(max_digits=6, decimal_places=2)
    note=models.CharField(max_length=120)
    state=models.CharField(max_length=1, choices=STATES)
    invoice=models.FileField(upload_to='uploads/',null=True)
    tracking_number=models.CharField(max_length=120,null=True)
    creation_date=models.DateTimeField(auto_now=True)



    payment_receipt=models.FileField(upload_to='uploads/',null=True)
    is_read=models.BooleanField(default=False)
    def sub_total(self):
        sub_total=0
        if self.cupon:
            sub_total=float(self.cart.total())-(float(self.cart.total())*(self.cupon.discount/100))
        else:
            sub_total=self.cart.total()

        return sub_total