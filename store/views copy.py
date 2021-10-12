from django.http import request
from django.shortcuts import render

from django.views.generic import TemplateView
from products.models import Product
from .models import Cart, CartItem
from products.models import Category

from django.contrib.sessions.models import Session
import json
from django.http import JsonResponse
from django.views.generic import ListView
from itertools import chain
class index(TemplateView):
    template_name='index.html'


    def get_context_data(self, **kwargs):
        print(self.request.session.get('is_checking',None))

        print("Session Id--------------------------------------------------------")
        print(self.request.session.session_key)

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of the first 16 elements always a multiple of four
        context['products'] = Product.objects.all()[:16]

        #Novidades
        #procurar os produtos novidade --- a rever
        novidades_queryset=Product.objects.all()
        #Incializar array
        novidades=[]
        


        #Separar num array em grupos de 5 para renderizar no carrousel

        novidades.append(novidades_queryset[:5])
        novidades.append(novidades_queryset[5:10])
        novidades.append(novidades_queryset[10:15])

        #print(novidades)
        print("123")
        #update ao contexto
        context['novidades']=novidades
        #promoções

             #procurar os promoções --- a rever
        promotions=Product.objects.all()
       


        #Separar num array em grupos de 5 para renderizar no carrousel 
        #update do contexto

        context['promotions']=promotions[:3]


        print(context['products'])
        return context




#products

#product details
def product_view(request,pk):
    print("from product view")
    product=Product.objects.get(pk=pk)
    return render(request, 'products/product.html',{"product":product})

#cart

#ajax






#add to cart

def ajax_add_cart(request,pk):
    add_flag=False
    products=Product.objects.filter(pk=pk)
    product=Product.objects.get(pk=pk)
    print(f'product:{ product }')
    # print(f'session cart---------------------------{request.session["cart"]}')

    if request.session.get('cart',None):
        cart=Cart.objects.get(pk=request.session.get('cart'))

        items=cart.items.all()
        for item in items:
            print(f'for loop in ajax add cart{item}')

            if item.product==product:
                item.quantity+=1
                item.save()
                add_flag=True
                print(f'Existe produto-{item.quantity}')
        if add_flag==False:
            print(f"nao existe produto")
            cart_item=CartItem(product=product)
            cart_item.save()
            cart.items.add(cart_item)

        print(f'Já tem sessao')
        print(f'cart:-----------{cart}')

    else:
        cart_item=CartItem(product=product)
        cart_item.save()
        print(f'cart_Item----------------:{cart_item}')
        session=Session.objects.get(session_key=request.session.session_key)
        cart=Cart.create(session)
        print(f'cart----------------:{cart}')
        cart.items.add(cart_item)

        request.session['cart']=cart.pk
        
    return render(request,'cart/main.html', {'cart':cart})


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
    print(f'{request}{pk}{type}')
    print("from ajax_update_qty_cart")
    cart=Cart.objects.get(pk=request.session.get('cart'))
    items=cart.items.all()

    for item in items:
        if item.pk==pk:
            if type == 'add':
                item.quantity+=1
                print("from ajax_update_qty_cart  -------add")

            elif type=='minus':
                if item.quantity==1:
                    return ajax_remove_item_cart(request,pk)
                item.quantity-=1
                
                print("from ajax_update_qty_cart  -------minus")
            item.save()
            data={"qty":item.quantity,"total":str(cart.total())}
            break
            
            
    else:
        pass
    

    dataJson=json.dumps(data)

        #print("view!!!")
        #print(data)
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
    # for key in categories:
        
    #     temp_categories=[key.pk]
    #     category=Category.objects.get(pk=key.pk)
    #     depth=category.depth+1
    #     categories_filter=Category.objects.filter(pk=key.pk)
    #     temp_categories.append(category.pk)
    #     while(True):
    #         print("Antes do inicio do loppppppppppppppppppppppppppppppppppppppppppppp")
    #         if Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories).exists():
    #             print("inicio do loppppppppppppppppppppppppppppppppppppppppppppp")
                
    #             categories_final=categories_final.union(categories_filter)
                
    #             #print(f'Condition {Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)}')
    #             categories_filter=Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)

    #             #print(f'categories filtert {categories_filter}')
    #             for category1 in categories_filter:
    #                 temp_categories.append(category1.pk)
    #             #print(f'temp categories after loop{temp_categories}')
    #             categories_final=categories_final.union(categories_filter)

    #             depth+=1 
    #             if not Product.objects.filter(category__in=temp_categories).exists():
                    
    #                 categories_del.append(key.pk)
    #             #temp_categories.clear()
    #         else:
    #             print(f"{temp_categories}break no loopppppppppppppppppppppppppppppp")
    #             print(Product.objects.filter(category__in=temp_categories))

    #             for key1 in Product.objects.filter(category__in=temp_categories):
    #                 print("aqui")
    #                 print(key1.category)
    #             if not Product.objects.filter(category__in=temp_categories).exists():
    #                 print("if dentro do loop")
    #                 for key1 in temp_categories:
    #                     print(key1)
    #                     categories_del.append(key1)

    #             #print(f'temp categories on break{temp_categories}')
    #             break     
    # categories=categories.exclude(id__in=categories_del)
    print(f'Categories from last line of base vieew------------------------------------------------------------------------------------------------{categories_del}')
    categories=filter(filter_categories,categories)
    return render(request,'ajax/categories.html', {'categories':categories})




def product_list_base(request,category=None):
    title="Ver todos"
    category_intance=False


    if not category:
        categories=Category.objects.filter(depth=0)
    else:
        category_intance=Category.objects.get(pk=category)
        categories=Category.objects.filter(parentPk=category_intance.pk)
        title=category_intance.name


    categories_final=Category.objects.none()
    categories_del=[]
    for key in categories:
        
        temp_categories=[key.pk]
        category=Category.objects.get(pk=key.pk)
        depth=category.depth+1
        categories_filter=Category.objects.filter(pk=key.pk)
        temp_categories.append(category.pk)
        while(True):
            print("Antes do inicio do loppppppppppppppppppppppppppppppppppppppppppppp")
            if Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories).exists():
                print("inicio do loppppppppppppppppppppppppppppppppppppppppppppp")
                
                categories_final=categories_final.union(categories_filter)
                
                #print(f'Condition {Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)}')
                categories_filter=Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)

                #print(f'categories filtert {categories_filter}')
                for category1 in categories_filter:
                    temp_categories.append(category1.pk)
                #print(f'temp categories after loop{temp_categories}')
                categories_final=categories_final.union(categories_filter)

                depth+=1 
                if not Product.objects.filter(category__in=temp_categories).exists():
                    
                    categories_del.append(key.pk)
                #temp_categories.clear()
            else:
                print(f"{temp_categories}break no loopppppppppppppppppppppppppppppp")
                print(Product.objects.filter(category__in=temp_categories))

                for key1 in Product.objects.filter(category__in=temp_categories):
                    print("aqui")
                    print(key1.category)
                if not Product.objects.filter(category__in=temp_categories).exists():
                    print("if dentro do loop")
                    for key1 in temp_categories:
                        print(key1)
                        categories_del.append(key1)

                #print(f'temp categories on break{temp_categories}')
                break     
    categories=categories.exclude(id__in=categories_del)
    print(f'Categories from last line of base vieew------------------------------------------------------------------------------------------------{categories_del}')
    return render(request,"products/list.html",{'categories' : categories, 'title':title, 'category':category_intance} )


class ProductListView(ListView):
    model=Product
    template_name="ajax/ajax-list.html"

    def get_queryset(self):
        json_raw=self.request.GET.get('json',None)
        queryset=Product.objects.all()
        categories_filter=None
        if json_raw:
            filters=json.loads(json_raw)
            print(filters)
            if filters['category']!=[-1]:
                # categories_filter=Category.objects.filter("")

                categories_final=Category.objects.none()

                for key in filters['category']:
                    
                    temp_categories=[]
                    category=Category.objects.get(pk=key)
                    depth=category.depth+1
                    categories_filter=Category.objects.filter(pk=key)
                    temp_categories.append(category.pk)
                    while(True):
                        if Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories).exists():
                            categories_final=categories_final.union(categories_filter)
                            
                            print(f'Condition {Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)}')
                            categories_filter=Category.objects.filter(depth=depth).filter(parentPk__in=temp_categories)

                            print(f'categories filtert {categories_filter}')
                            temp_categories.clear()
                            for category1 in categories_filter:
                                temp_categories.append(category1.pk)
                            print(f'temp categories after loop{temp_categories}')
                            categories_final=categories_final.union(categories_filter)

                            depth+=1 
                            
                        else:
                            categories_final=categories_final.union(Category.objects.filter(pk__in=temp_categories))
                            print(f'temp categories on break{temp_categories}')
                            break       

                print(f'Categorial FINALLLLLLLLLLLLLLLLLLLLLLLLLL {categories_final}')



                categories_id=[]
                for category in categories_final:
                    categories_id.append(category.pk)

                queryset=queryset.filter(category__in=categories_id)


            print(filters)
            if 'orderby' in filters:
                if filters['orderby']=='price':
                    if filters['orderby_dir']=='desc':
                        queryset=queryset.order_by('-price')
                    else:
                        queryset=queryset.order_by('price')
        return queryset