from celery import shared_task
from celery import Celery

from store.models import Cart
from products.models import Product
from django.contrib.sessions.backends.db import SessionStore


from django.contrib.sessions.models import Session
from django.core.mail import EmailMessage
from albiclick.ifthenpay import verifyMbway
app = Celery('tasks', broker='redis://localhost')

@app.task
def add(x, y):
    return x + y


@app.task
def update_stock(cart):
    print("form update stock celery")
    
    cart=Cart.objects.get(pk=cart)
    print(f' is checked out={cart.is_checked_out}')

    if cart.is_checked_out == False:
        s1=Session.objects.get(session_key=cart.session)
        #print(cart.session)

        s=SessionStore(session_key=s1.pk)
        #print(s)

        items=cart.items.all()


        for item in items:

            stock=item.product.stock+item.quantity
            item.product.stock=stock
            item.product.save()

            print(item.product.stock)
        cart.is_timed_out=True
        cart.save()
        print(f'is timed out={cart.is_timed_out}')
        # s['checkout'] = False
        del s['checkout']
        s.save()

    return "Tsete"

@app.task
def task_verifymbway(id):
    return verifyMbway(id)

# @app.task
# def send_mail(subject, html_message, from_email,at):
#     print("from task!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#     email=EmailMessage(subject, html_message, from_email)
    
#     email.send()