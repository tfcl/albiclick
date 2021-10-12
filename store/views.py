from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.conf import path

from django.views.generic import TemplateView
from products.models import Product
from .models import Cart, CartItem
from products.models import Category

from django.contrib.sessions.models import Session
import json
from django.http import JsonResponse
from django.views.generic import ListView
from itertools import chain
from django.db.models import Avg, Max, Min
from django.core import serializers
from django.contrib.postgres.search import TrigramSimilarity
class index(TemplateView):

 
    template_name='index.html'


    def get_context_data(self, **kwargs):
        #print(self.request.session.get('is_checking',None))

        #print("Session Id--------------------------------------------------------")
        #print(self.request.session.session_key)

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of the first 16 elements always a multiple of four
        context['products'] = Product.objects.all()[:16]

        #Novidades
        #procurar os produtos novidade --- a rever
        novidades_queryset=Product.objects.all()
        #Incializar array
        novidades=Product.objects.filter(new=True)
        destaques=Product.objects.filter(highlighted=True)


        #Separar num array em grupos de 5 para renderizar no carrousel

       

        ##print(novidades)
        #print("123")
        #update ao contexto
        context['novidades']=novidades
        context['destaques']=destaques

        #promoções

             #procurar os promoções --- a rever
        promotions=Product.objects.all()
       


        #Separar num array em grupos de 5 para renderizar no carrousel 
        #update do contexto

        context['promotions']=promotions[:3]


        #print(context['products'])
        return context




#products

#product details
def product_view(request,pk):
    #print("from product view")
    product=Product.objects.get(pk=pk)

    get_path_categories(product.category)

    return render(request, 'products/product.html',{"product":product,"path": get_path_categories(product.category)})

#cart

#ajax






#add to cart

def ajax_add_cart(request,pk):
    cart=None
    error=None
    add_flag=False
    products=Product.objects.filter(pk=pk)
    product=Product.objects.get(pk=pk)
    #print(f'product:{ product }')
    # #print(f'session cart---------------------------{request.session["cart"]}')
    if not request.session or not request.session.session_key:
        request.session.save()
    if request.session.get('cart',None):
        cart=Cart.objects.get(pk=request.session.get('cart'))

        items=cart.items.all()
        for item in items:
            #print(f'for loop in ajax add cart{item}')

            if item.product==product:
                item.quantity+=1

                if item.quantity>item.product.stock:
                    error="Ultrapassou o stock"
                else:
                    item.save()

                add_flag=True
                #print(f'Existe produto-{item.quantity}')
        if add_flag==False:
            #print(f"nao existe produto")
            cart_item=CartItem(product=product)

            if cart_item.quantity>cart_item.product.stock:
                error="Ultrapassou o stock"
            else:

                cart_item.save()
                cart.items.add(cart_item)

        #print(f'Já tem sessao')
        #print(f'cart:-----------{cart}')

    else:
        cart_item=CartItem(product=product)

        if cart_item.quantity>cart_item.product.stock:
            error="Ultrapassou o stock"
            session=Session.objects.get(session_key=request.session.session_key)
            cart=Cart.create(session)
            request.session['cart']=cart.pk

        else:

            cart_item.save()
        #print(f'cart_Item----------------:{cart_item}')
            session=Session.objects.get(session_key=request.session.session_key)
            cart=Cart.create(session)
            #print(f'cart----------------:{cart}')
            cart.items.add(cart_item)

            request.session['cart']=cart.pk
        
    return render(request,'cart/main.html', {'cart':cart,'error':error})


#remove product from cart

def ajax_remove_item_cart(request,pk):
    cart=Cart.objects.get(pk=request.session.get('cart'))
    items=cart.items.all()

    for item in items:
        if item.pk==pk:
            cart.items.remove(item)
            break
    if cart.items.all():    
        return render(request,'cart/main.html', {'cart':cart})
    else:
        return ajax_clean_cart(request)
#update qty from product


def ajax_update_qty_cart(request,pk,type):
    #print(f'{request}{pk}{type}')
    #print("from ajax_update_qty_cart")
    cart=Cart.objects.get(pk=request.session.get('cart'))
    items=cart.items.all()

    for item in items:
        if item.pk==pk:
            if type == 'add':
                item.quantity+=1

                
                if item.quantity>item.product.stock:
                    return HttpResponse(-1)
                
                #print("from ajax_update_qty_cart  -------add")

            elif type=='minus':
                if item.quantity==1:
                    return ajax_remove_item_cart(request,pk)
                item.quantity-=1
                
                #print("from ajax_update_qty_cart  -------minus")
            item.save()
            data={"qty":item.quantity,"total":str(cart.total())}
            break
            
            
  

    dataJson=json.dumps(data)

        ##print("view!!!")
        ##print(data)
    return JsonResponse(dataJson,safe=False)


#delete cart 

def ajax_clean_cart(request):
    cart=Cart.objects.get(pk=request.session.get('cart'))
    cart.delete()
    del request.session['cart']
    
    
    return render(request,'cart/main.html')


def ajax_get_cart(request):
    cart=Cart.objects.get(pk=request.session.get('cart'))
    return render(request,'cart/main.html',{'cart':cart})



#load categories on menu





#check if queryset of categories has products associated


def filter_categories(category_intance):
        depth=category_intance.depth+1
        temp_categories=[category_intance.pk]


        while(True):
            
            categories_filter=Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)
            if categories_filter.exists():
                for elem in categories_filter:
                    temp_categories.append(elem.pk)
                depth+=1 


            else:
                break     

        if Product.objects.filter(category__in=temp_categories).exists():   
            return True
        else: 
            return False  

def ajax_load_categories(request):

    categories=Category.objects.filter(depth=0)
    categories_final=Category.objects.none()
    categories_del=[]
   
    #print(f'Categories from last line of base vieew------------------------------------------------------------------------------------------------{categories_del}')
    categories=filter(filter_categories,categories)
    return render(request,'ajax/categories.html', {'categories':categories})


def get_related_categories(category_pk):
    categories=[]
    temp_categories=[]

    category=Category.objects.get(pk=category_pk)
    depth=category.depth+1
    temp_categories.append(category.pk)
    categories.append(category_pk)
    while(True):
        if Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories).exists():
            
            #print("existe")
            categories_queryset=Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)
            
            temp_categories.clear()
            #print(f"categories_queryset{categories_queryset}")
            for category1 in categories_queryset:
                #print("loop")
                categories.append(category1.pk)
                temp_categories.append(category1.pk)
            depth+=1
            #print(categories)
        else:
            break

    #print(f"catgeorias:::::::::::::::::::::::::::::::{categories}")

    
    return categories

def get_path_categories(category):
    categories=[]

    categories.append(category)
    while(True):
        if category.depth!=0:
            category=category.parentPk
            categories.append(category)
           
        else:
            break

    print(f"Get Cateories path!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{categories}")

    categories.reverse()
    return categories
def product_list_destaques(request):
    title="Destaques"
    ##print("product_list_destaques")


    return render(request,"products/list.html",{'title':title} )



def product_list_base(request,category="-1"):
    title="Ver todos"
    category_intance=False
    categories=None
   
    flag_destaques=False
    flag_novidades=False
    category_path=None
    flag_search=request.GET.get("search",False)
    



    if flag_search != False:
        title=flag_search
    else:
        if category=="-1":

            categories=Category.objects.filter(depth=0)
            categories=filter(filter_categories,categories)
            
        elif category.isnumeric():
            
            
            category_intance=Category.objects.get(pk=category)
            categories=Category.objects.filter(parentPk=category_intance.pk)
            title=category_intance.name

            categories=filter(filter_categories,categories)
            category_path=get_path_categories(category_intance)
        else:
            
            
            if category=='destaques':
                flag_destaques=True
                title="Destaques"
                


            elif category=='novidades':
                flag_novidades=True
                title="Novidades"

        
            
    return render(request,"products/list.html",{'categories' : categories, 'title':title, 'category':category_intance,'flag_destaques':flag_destaques,'flag_novidades':flag_novidades,'category_path':category_path,'flag_search':flag_search} )


class ProductListView(ListView):
    model=Product
    template_name="ajax/ajax-list.html"
    paginate_by = 16
    queryset=None

    flag_first_load=False
    flag_destaques=False
    flag_novidades=False
    flag_search=False



    def get_queryset(self):
        json_raw=self.request.GET.get('json',None)
        queryset=Product.objects.all()
        categories_filter=None
        categories_id=[]



        if json_raw:
            filters=json.loads(json_raw)
            print(f"filtersssssssssssssssssssssssssssss{filters}")
            if 'flag_first_load' in filters:
                self.flag_first_load=True
            if 'flag_destaques' in filters:
                
                queryset=Product.objects.filter(highlighted=True)
                self.queryset=queryset   
                self.flag_destaques=True     

            elif 'flag_novidades' in filters:
                queryset=Product.objects.filter(new=True)
                self.queryset=queryset   
                self.flag_novidades=True

            elif 'search_filter' in filters:
            
                queryset=Product.objects.annotate(similarity=TrigramSimilarity('name', filters['search_filter']),).filter(similarity__gt=0.1).order_by('-similarity')
                self.flag_search=filters['search_filter']
                self.queryset=queryset   

            if filters['category']!=[-1] :
                # categories_filter=Category.objects.filter("")

                

                for key in filters['category']:
                    for category_temp in get_related_categories(key):
                        categories_id.append(category_temp)

                #print(f"aqui!!!!!!!!!!!!!!!!!!!!{categories_id}")
                queryset=queryset.filter(category__in=categories_id)


            #print(filters)
            if 'orderby' in filters:
                if filters['orderby']=='price':
                    if filters['orderby_dir']=='desc':
                        queryset=queryset.order_by('-price')
                    else:
                        queryset=queryset.order_by('price')
            if 'price-filter' in filters:
                price_filter=filters['price-filter']
                queryset=queryset.filter(price__gte=price_filter[0],price__lte=price_filter[1])


        #print(f"last_line{queryset}")        
        self.queryset=queryset        
        return queryset



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dict_categories={}
        queryset=self.queryset
        
        context.update(queryset.aggregate(Min('price')))
        context.update(queryset.aggregate(Max('price')))
        if self.flag_first_load==True:
            context['flag_first_load']=True

        if self.flag_destaques==True or self.flag_novidades==True or self.flag_search!=False:
            print("in if statment !!!!!!!!!!!!!")
            categories=[]
            for object in queryset:
                categories.append(object.category.pk)
            categories_queryset=Category.objects.filter(id__in=categories)

            for object in categories_queryset:
                dict_categories[object.pk]=object.name
            context['categories']=json.dumps(dict_categories)
            print(f"categories!!!!!!!!!!!!!!!!!!!!!{context['categories']}")
            
            if self.flag_destaques==True:

                context['flag_destaques']=True
            elif self.flag_novidades==True:
                context['flag_novidades']=True
            elif self.flag_search!=False:
                context['flag_search']= True
            
        print(f"context!!!!!!!!!!!!!!!!!!!!{context}")
        return context
        