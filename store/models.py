from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from products.models import Product
from django.contrib.sessions.models import Session
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    

    def total(self):
        return self.quantity * self.product.price
    @classmethod
    def create(cls, product):
        cart_item = cls(product=product)
        print(f'from cartItem create{cart_item}')
       # do something with the book
        return cart_item



class Cart(models.Model):
    session= models.ForeignKey(Session, on_delete=models.SET_NULL,null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    items=models.ManyToManyField(CartItem)

    is_checked_out=models.BooleanField(default=False)
    is_timed_out=models.BooleanField(default=False)
    def total(self):
        total=0
        for item in self.items.all():
            total+=item.product.price*item.quantity
        return total
    @classmethod
    def create(cls, session):
        cart = cls(session=session)
        
        cart.save()
        print(f'from cart create{cart}')
       # do something with the book
        return cart