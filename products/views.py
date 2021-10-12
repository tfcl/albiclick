from django import http
from django.core.files.base import File
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from rest_framework import viewsets
from .serializers import ProductSerializer
from .models import Product,Category,Image
from .forms import CreateProduct, UpdateImage

from io import BytesIO
from django.core.files.storage import FileSystemStorage

from django.http import JsonResponse, request
from django.core import serializers
import json
from django.forms import modelformset_factory

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
# Create your views here.

def create(request):

    if request.method == "GET":
        categories=Category.objects.filter(depth=0)
        form=CreateProduct()

        return render(request,'create.html',{'form':form,'categories':categories})


    if request.method == "POST":
        form=CreateProduct(data=request.POST, files=request.FILES)
        

        specs=json.loads(request.POST["json-specs"])
        ##print(specs)
        


        if form.is_valid():
            new=form.save()
            # ##print(f'FILES----------------------{request.FILES.getlist('images')}')
            fs = FileSystemStorage()
            print(request.FILES.getlist('images'))
            for image in request.FILES.getlist('images'):
                
                filename = fs.save(image.name, image)
                new.image_set.create(image=filename)
            for key in specs:
                ##print(key, '->', specs[key])
                new.spec_set.create(name=key, spec=specs[key])


            ##print(form.instance.pk)
            return redirect('index')
        else:
            ##print (f'form: {form.errors["category"]}')
            return render(request,'create.html',{'form':form,'categories':Category.objects.filter(depth=0)})




def update_product(request, pk):
    product=Product.objects.get(pk=pk)
    images=product.image_set.all()
    categories=[]
    categories_temp=[]
    category=product.category
    images_initial=[]
    UpdateImageFormset=modelformset_factory(
            Image,form=UpdateImage,can_delete=True)
    while True:
        #print(f"loop{category.depth} {category.name}")
        if category.depth !=0:
            parent=Category.objects.get(pk=category.parentPk.pk)
            categories_temp=Category.objects.filter(depth=category.depth).filter(parentPk=parent)
          
            categories.insert(0,categories_temp)
            category=parent
        else:
            categories_temp=Category.objects.filter(depth=category.depth)
            categories.insert(0,categories_temp)
            break

   
    


    if request.method == "GET":
        initial_dict={
            "name": product.name,
            "description":product.description,
            "detail":product.detail,
            "price":product.price,
            "stock":product.stock,
            "category":product.category,
            "highlighted":product.highlighted,
            "new":product.new,
            "main_image":product.main_image




        }
        
        form=CreateProduct(initial=initial_dict)

        formset_images=UpdateImageFormset(queryset=images,prefix='images')
        #print(formset_images)
        return render(request,'update.html',{'form':form,'form_images':formset_images,"categories":categories})

    if request.method == "POST":
        forms=[]

        form=CreateProduct(data=request.POST, files=request.FILES,instance=product)
        

        form_images=UpdateImageFormset(data=request.POST, files=request.FILES,prefix='images')
     
       
        if form.is_valid() and form_images.is_valid():
            new=form.save()
            for form in form_images:
                
                form.save()
                
            fs = FileSystemStorage()
            for image in request.FILES.getlist('images'):
            
                filename = fs.save(image.name, image)
                new.image_set.create(image=filename)

            
            return redirect('index')
        else:
            return render(request,'update.html',{'form':form,'form_images':form_images,'categories':Category.objects.filter(depth=0)})



def ajax_delete_image(request):
    pk=request.GET.get("pk",None)
    print(pk)
    Image.objects.get(pk=int(pk)).delete()
    return HttpResponse("sucess")

def ajax_delete_product(request):
    pk=request.GET.get("pk",None)
    
    Product.objects.get(pk=int(pk)).delete()
    return HttpResponse("sucess")

    


def load_categories(request):
    
    ###print("load categories")



    categoriesHtml=[]
    categoriesAll=[]
    category_id = request.GET.get('category')
    
    
    category=Category.objects.get(id=category_id)
    
    categories=Category.objects.filter(parentPk=category)


    ##print(categories)

    return JsonResponse(serializers.serialize('python', categories),safe=False)