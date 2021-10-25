from django import http
from django.http.response import HttpResponse
from administrator.views import order
import re
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
import json
from django.http import JsonResponse

from store.models import Cart
from .models import Cupon, Order, Shipment, Payment, Detail
from users.models import Adress

from .tasks import update_stock, task_verifymbway
from django.contrib import messages


from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from albiclick.ifthenpay import payshop,mbway,verifyMbway,generateMbRef

import time
from django.urls import reverse
from albiclick.celery import app



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





def calculate_total(cart,shipment,cupon=None):
    total=cart.total()
    if cupon:
        total=float(total)-(float(cart.total())*(cupon.discount/100))
        if cupon.is_free_shipping == False:
            total=float(total)+float(shipment.price)
            
    else:
      total=float(total)+float(shipment.price)  
      
    return format(total,".2f")





def ajax_check_cupon(request):
    cod=request.GET.get("cupon")
    shipment_pk=request.GET.get("shipment_pk")
    shipment=Shipment.objects.get(pk=shipment_pk)
    cupon=Cupon.objects.get(code=cod)
    print(f"cupao {cupon}  shipment{shipment}")
    cart=Cart.objects.get(pk=request.session.get('cart'))
    total=float(cart.total())-(float(cart.total())*(cupon.discount/100))
    

    if cupon.is_free_shipping==True:
        pass
    else:
        total=total+shipment.price
    
    print(f"Total!!!!!!!!!!!!{total}")

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

    context={}

    cart=Cart.objects.get(pk=request.session.get('cart'))

    if check_time_out(cart, request) : return redirect('index')



    cart_items=cart.items.all()

    #para testes
    #update_stock.apply_async(args=(cart.pk,), countdown=60)

    if 'checkout' not in request.session:
        
        #update_stock.apply_async(args=(cart.pk,), countdown=3000)

        for item in cart_items:
            stock=item.product.stock-item.quantity
            item.product.stock=stock
            item.product.save()

        print(item.product.stock)

    
    request.session["checkout"]=True
    print(request.session["checkout"])
    context["adress"]=request.user.profile.adress
    context["adress_billing"]=request.user.profile.adress_billing
    context["cart"]=cart
    return render(request,'orders/checkout.html',context=context)



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
        print(request.POST)
        shipment=Shipment.objects.get(pk=int(request.POST.get('shipment')))
        cupon=None
        cart=Cart.objects.get(pk=request.session.get('cart'))
        if request.POST.get('cupon-code')!="":
            if Cupon.objects.filter(code=request.POST.get('cupon-code')).exists():
                cupon=Cupon.objects.get(code=request.POST.get('cupon-code'))


        total=calculate_total(cart,shipment,cupon)
        total=float(total)

        

        print(cart.session)
        #verificar se este save é necessario
        shipment=Shipment.objects.get(pk=int(request.POST.get('shipment')))
        adress=request.user.profile.adress
        adress_billing=request.user.profile.adress_billing
        note=request.POST.get('note')
        print(f'{shipment}{adress}{adress_billing}')    

        
        


        order=Order(cart=cart, adress=adress, adress_billing=adress_billing, shipment=shipment,note=note,total=total,cupon=cupon, user=request.user,state="1")  
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

            data=generateMbRef(str(order.pk),order.total)
            print(f"Referencia{data}")

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
            
            # ver_output=ver.get()
            # print(ver_output)
            # while(True):
            #     time.sleep(5)
            #     flag=verifyMbway(idPedido)
            #     print(flag)
            #     if flag != -1:
            #         break



            

            # if flag == False:
            #     order.delete()
            #     return HttpResponse("-1")



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




def get_cupon_details(cupon):
    cupon_dict={
        'discount':cupon.discount,
        'cupon':cupon.code,


    }

    if cupon.is_free_shipping==True:
        cupon_dict['free_shipment']=True
    else:
        cupon_dict['free_shipment']=False
 
    return cupon_dict

def ajax_get_total(request):
    print(request.GET)
    cart=Cart.objects.get(pk=request.session.get('cart'))
    total=0
    cod=request.GET.get("cupon")
    shipment_pk=request.GET.get("shipment")
    shipment=Shipment.objects.get(pk=shipment_pk)
    cupon=None
 
    context={}

    if cod != "" :
        if Cupon.objects.filter(code=cod).exists():

            cupon= Cupon.objects.get(code=cod)
            context=get_cupon_details(cupon)

        else:
  
            context['cupon_error']=False


   

    # print(dataJson)
    total=calculate_total(cart,shipment,cupon)
    context['total']=str(total)+" €"
    dataJson=json.dumps(context)
    
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

