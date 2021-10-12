from django import http
from django.http.response import HttpResponse
from administrator.views import order
import re
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
import json
from django.http import JsonResponse

from store.models import Cart
from .models import Order, Shipment, Payment, Detail
from users.models import Adress

from .tasks import update_stock
from django.contrib import messages


from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from albiclick.ifthenpay import payshop,mbway,verifyMbway,generateMbRef

import time
from django.urls import reverse




def check_user_order(view):
    def wrapper(request, *args, **kw):

        user=request.user
        order=Order.objects.get(pk=kw["pk"]) 

        if order.user == user:
            return view(request,kw["pk"])
        else:
            messages.add_message(request, messages.ERROR, 'Não tem permissões para aceder a essa página.')

            return redirect("dashboard-args",2)
        # print(f'args:{args}')
        # print(f'kwargs:{kw}')


    return wrapper













def check_time_out(cart,request):
    if cart.is_timed_out == True:
        cart.is_timed_out=False
        cart.save()
        messages.add_message(request, messages.ERROR, 'O seu checkout expirou, por favor tente de novo.')
        return True
    else:
        return False
        # return redirect('index')




@login_required(login_url='/customer/accounts/login/')
def checkout(request):

    

    cart=Cart.objects.get(pk=request.session.get('cart'))

    if check_time_out(cart, request) : return redirect('index')



    cart_items=cart.items.all()

    #para testes
    #update_stock.apply_async(args=(cart.pk,), countdown=60)

    if 'checkout' not in request.session:
        
        update_stock.apply_async(args=(cart.pk,), countdown=3000)

        for item in cart_items:
            stock=item.product.stock-item.quantity
            item.product.stock=stock
            item.product.save()

        print(item.product.stock)

    
    request.session["checkout"]=True
    print(request.session["checkout"])
    return render(request,'orders/checkout.html',{'cart':cart})


def payment(request):
    cart=Cart.objects.get(pk=request.session.get('cart'))
    if check_time_out(cart,request) : return redirect('index')

    if request.user.profile.adress==None:
        messages.add_message(request, messages.ERROR, 'Por favor verifique a Morada de Envio.')
        return redirect('checkout')
    if request.method == "GET":
        shipments=Shipment.objects.all()
        print(request.session["checkout"])
        return render(request,'orders/checkout-payments.html',{'shipments':shipments})

    if request.method == "POST":
        shipment=Shipment.objects.get(pk=int(request.POST.get('shipment')))
        total=cart.total()+shipment.price


        

        cart=Cart.objects.get(pk=request.session.get('cart'))
        print(cart.session)
        #verificar se este save é necessario
        shipment=Shipment.objects.get(pk=int(request.POST.get('shipment')))
        adress=request.user.profile.adress
        adress_billing=request.user.profile.adress_billing
        note=request.POST.get('note')
        print(f'{shipment}{adress}{adress_billing}')    

        
        


        order=Order(cart=cart, adress=adress, adress_billing=adress_billing, shipment=shipment,note=note,total=total, user=request.user,state="1")  
        print(f"order!!!!!!!!!!!!!!!!{order.cart}")
        order.save()
        method=request.POST.get("payment-method")

        if method=="payshop":
            payment=Payment(name="Payshop")
            payment.save()
            data=payshop( str(order.pk), str(order.total) )
            payment.detail_set.create(title="Referencia", description=data["Reference"])
            payment_flag=True


        if method=="mb":
            print(f'payment method MB')
            payment=Payment(name="Multibanco")
            payment.save()

            data=generateMbRef( str(order.pk), order.total )


            payment.detail_set.create(title="Entidade", description=data["Entidade"])
            payment.detail_set.create(title="Referencia", description=data["Referencia"])
            payment.detail_set.create(title="Valor", description=data["Valor"])
            

            details=payment.detail_set.all()
            for detail in details:
                print(f'{detail.title} {detail.description}')
            
            

            payment_flag=True
           
        elif method=="mbway":
            phone=request.POST.get('telemovel')
            print(phone)

            data=mbway(str(order.pk),str(order.total),phone,order.user.email)

            idPedido=data["IdPedido"]
            print(f"idPedidoo!!!!!!!!!!!!{idPedido}")


            time.sleep(5)
    


            flag=verifyMbway(idPedido)

            

            if flag == False:
                order.delete()
                return HttpResponse("-1")



            payment=Payment(name="MB Way")
            payment.save()
            payment.detail_set.create(title="Aviso", description="Iremos confimar o seu pagamento assim que possivél")
            payment_flag=True
            print(f'payment method MBway')

        elif method=="credit":
            payment=Payment(name="Credit")
            payment.save()
            print(f'payment method credit')
            payment_flag=True

        if payment_flag==True:
            order.payment=payment
            order.save(update_fields=["payment"])

            cart.session=None
            cart.is_checked_out=True
            cart.save()

            del request.session['cart']
            del request.session['checkout']

            print(order)


            if method=="mbway":
                
                return HttpResponse(order.pk)    
            return redirect('order-details', pk=order.pk)

            
            

            
            
        

@check_user_order
def order_details(request,pk):
       ##teste
    # print(payshop("5","50.00"))
    # print(mbway("5","5.00","965105224","tiago9l@hotmail.com"))




    ##

    order=Order.objects.get(pk=pk)

    return render(request, 'orders/details.html', {'order':order})





def ajax_get_total(request, pk):
    cart=Cart.objects.get(pk=request.session.get('cart'))
    shipment=Shipment.objects.get(pk=pk)

    total=cart.total()+shipment.price

    dataJson=json.dumps({'total':str(total)+" €"})

  
    return JsonResponse(dataJson,safe=False)
def ajax_payment_mb(request):
    return render(request,'ajax/payments/mb.html')

def ajax_payment_mbway(request):
    return render(request,'ajax/payments/mbway.html')

def ajax_payment_credit(request):
    return render(request,'ajax/payments/credit.html')

def ajax_payment_payshop(request):
    return render(request,'ajax/payments/payshop.html')

def ajax_get_unread(request):
    unread=Order.objects.filter(is_read=False).count()

    return HttpResponse(unread)

