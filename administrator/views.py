# from django.db.models.aggregates import Sum
from store.models import Cart, CartItem
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from orders.models import Order,Shipment
from products.models import Product
from django.views.generic import ListView
from . import forms
import json
from django.db.models import Count, F, Subquery, Sum,OuterRef
from django.contrib import messages
from django.contrib.auth.models import User
from albiclick.queries import get_products
from orders.forms import CreateCupon
from orders.models import Cupon
import datetime
from django.utils.timezone import make_aware

def check_admin(view):
    def wrapper(request, user=None):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return view(request)
            else:
                messages.add_message(request, messages.ERROR, 'Não tem permissões para aceder a essa página.')
                
                return redirect('index')

        else:
            return redirect('login')
    return wrapper





class CheckAdminMixin:

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)

            else:
                messages.add_message(request, messages.ERROR, 'Não tem permissões para aceder a essa página.')
                
                return redirect('index')

        else:
            return redirect('login')





@check_admin
def administrator(request):

    return render(request,'administrator/administrator.html')


def orders(request):
    return render(request, 'administrator/orders.html')



def products(request):
    return render(request, 'administrator/products.html')


def users(request):
    return render(request, 'administrator/users.html')

def ajax_desactivate_cupon(request):
    pk=request.GET.get("pk")
    cupon=Cupon.objects.get(pk=pk)

    if cupon.is_active:
        cupon.is_active=False
        cupon.save()
    return HttpResponse()

def ajax_activate_cupon(request):
    pk=request.GET.get("pk")
    cupon=Cupon.objects.get(pk=pk)

    if not cupon.is_active:
        cupon.is_active=True
        cupon.save()
    return HttpResponse()


def update_cupon(request, pk):
    cupon=Cupon.objects.get(pk=pk)
    if request.method == "GET":
        form=CreateCupon(initial={"code":cupon.code, "discount":cupon.discount,"is_free_shipping":cupon.is_free_shipping,"max_redeem":cupon.max_redeem})
        return render(request,'cupon/create.html',{'form':form})
            

    if request.method == "POST":
        form=CreateCupon(request.POST,instance=cupon)
        if form.is_valid():
            form.save()
            return redirect("administrator-cupons")
        else:
            return render(request,'cupon/create.html',{'form':form})
def create_cupon(request):


            

    
    if request.method=='GET':
        form=CreateCupon()
        return render(request,'cupon/create.html',{"form":form})
    elif request.method=='POST':
        form=CreateCupon(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administrator-shipments")
        else:
            return render(request,'cupon/create.html',{'form':form})
       

class CuponsListView(CheckAdminMixin ,ListView):
    model=Cupon
    template_name="cupon/cupons.html"

class ShipmentsListView(CheckAdminMixin ,ListView):
    model=Shipment
    template_name="administrator/shipments.html"
    
class UsersListView(CheckAdminMixin ,ListView):
    model=User
    template_name="ajax/users-list.html"
    

class ProductListView(CheckAdminMixin ,ListView):
    model=Product
    template_name="ajax/product-list.html"
    paginate_by = 20

    def get_queryset(self):
        
        queryset=get_products()
        
        json_raw=self.request.GET.get('json',None)

        filter_ids=Product.objects.none()
        flag_filters=False
        if json_raw:
            filters=json.loads(json_raw)
            print(filters)
            if 'search' in filters:
                
                queryset=queryset.filter(pk=filters["search"])
            if 'filters' in filters:
                flag_filters=True
                if 'stock' in filters['filters']:
                    
                    filter_ids=filter_ids.union(queryset.filter(stock__gte=1).values_list('pk',flat=True))
                    

                    print("in stock")

                if '!stock' in filters['filters']:
                    filter_ids=filter_ids.union(queryset.filter(stock__lte=0).values_list('pk',flat=True))

                    print("without stock")
                if 'sells' in filters['filters']:

                    filter_ids=filter_ids.union(queryset.filter(num_sells__gte=1).values_list('pk',flat=True))

                    print("in sells")

                if '!sells' in filters['filters']:
                    print(queryset.filter(num_sells=0).values_list('pk',flat=True))
                    print(queryset.get(pk=6).num_sells)
                    filter_ids=filter_ids.union(queryset.filter(num_sells=None).values_list('pk',flat=True))

                    print("without sells")
                        
            if flag_filters:
                queryset=queryset.filter(id__in=filter_ids)

                

            if 'order_by' in filters:
                print("degub!!!!!!!!!!!!!!!!!!!!!!!!!!")
                
                if filters['order_by']=='price':
                    
                    if filters['orderby_dir']=='asc':
                        queryset=queryset.order_by('price')
                    else:
                        queryset=queryset.order_by('-price')
                                               
                elif filters['order_by']=='stock':
                    if filters['orderby_dir']=='asc':
                        queryset=queryset.order_by('stock')
                    else:
                        queryset=queryset.order_by('-stock')                            
                            
                elif filters['order_by']=='sells':
                    if filters['orderby_dir']=='asc':
                        queryset=queryset.order_by('num_sells')
                    else:
                        queryset=queryset.order_by('-num_sells')                            
                print("order_by")
        print(filter_ids)
        return queryset

class OrderListView(ListView):
    model=Order
    template_name="ajax/order-list.html"
    paginate_by = 20


    def get_queryset(self):
        queryset=Order.objects.all().order_by('-creation_date')
        json_raw=self.request.GET.get('json',None)

        if json_raw:
            filters=json.loads(json_raw)
            print(filters)



            if 'filters' in filters:
                
                print(filters['filters'])

                queryset=queryset.filter(state__in=filters['filters'])
                    
            if 'date-start' in filters and 'date-end' in filters:
               
                print(filters['date-start'])
                print(filters['date-end'])
                date_start=make_aware(datetime.datetime.strptime(filters['date-start'], '%Y-%m-%d'))
                date_end=make_aware(datetime.datetime.strptime(filters['date-end'], '%Y-%m-%d'))

                print(f'Data Inicio{date_start}')
                queryset=queryset.filter(creation_date__gte=date_start,creation_date__lte=date_end)
            elif 'date-start' in filters:
                date_start=make_aware(datetime.datetime.strptime(filters['date-start'], '%Y-%m-%d'))
                time_change = datetime.timedelta(hours=23, minutes=59, seconds=59)
                date_end=date_start+time_change
                print(f'Data fim{date_end}')
                
                queryset=queryset.filter(creation_date__gte=date_start,creation_date__lte=date_end)

                print(filters['date-start'])




            if 'search' in filters:
                queryset=queryset.filter(pk=filters['search'])





        if 'order_by' in filters:
            if filters['order_by']=='total':
                if filters['orderby_dir']=='asc':
                    queryset=queryset.order_by('total')
                else:
                    queryset=queryset.order_by('-total')
                    
            if filters['order_by']=='date':
                if filters['orderby_dir']=='asc':
                    queryset=queryset.order_by('creation_date')
                else:
                    queryset=queryset.order_by('-creation_date')
        return queryset

def order(request, pk):

    order=Order.objects.get(pk=pk)

    if not order.is_read:
        order.is_read=True
        order.save()

    return render(request, 'administrator/order.html',{'order':order})

def update_order(request, pk):
    print("aqui")
    instance=Order.objects.get(pk=pk)

    if request.method=='GET':
        if instance.state=="1":
            form=forms.UpdateOrder1(initial={'state':'2'})
            
        elif instance.state=="2":
            form=forms.UpdateOrder2(initial={'state':'3'})

        elif instance.state=="3":
            form=forms.UpdateOrder3(initial={'state':'4'})


    elif request.method=='POST':
        if instance.state=="1":
            form=forms.UpdateOrder1(data=request.POST, files=request.FILES, instance=instance)

        elif instance.state=="2":
            form=forms.UpdateOrder2(data=request.POST, files=request.FILES, instance=instance)

        elif instance.state=="3":
            form=forms.UpdateOrder3(data=request.POST, files=request.FILES, instance=instance)



        if request.FILES:

            print(request.FILES)
        else:
            print("Sem ficheiros")



        if form.is_valid():
            new=form.save(commit=False)
            new.save(update_fields=['state'])
            print(f"Invoice!!!!!!!!!!!!!!{new.invoice}")
            print(new)
            return HttpResponse("1")
            print(f'pagamento confirmado{form}')
      
    print(instance.state)
    return render(request,'administrator/update-order.html', {'form':form, 'order':instance})


def cancel_order(request, pk):
    order=Order.objects.get(pk=pk)
    order.state="0"
    order.save(update_fields=['state',])
    return redirect('administrator-order', pk=order.pk)

def ajax_delete_shipment(request):
    pk=request.GET.get("pk",None)
    
    Shipment.objects.get(pk=int(pk)).delete()
    return HttpResponse()


def create_shipment(request):
    if request.method == "GET":
        form=forms.ShipmentForm()
        return render(request,'shipment/create.html',{'form':form})
            

    if request.method == "POST":
        form=forms.ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("administrator-shipments")
        else:
            return render(request,'shipment/create.html',{'form':form})



def update_shipment(request,pk):
    shipment=Shipment.objects.get(pk=pk)
    if request.method == "GET":
        form=forms.ShipmentForm(initial={"name":shipment.name, "price":shipment.price})
        return render(request,'shipment/create.html',{'form':form})
            

    if request.method == "POST":
        form=forms.ShipmentForm(request.POST,instance=shipment)
        if form.is_valid():
            form.save()
            return redirect("administrator-shipments")
        else:
            return render(request,'shipment/create.html',{'form':form})
