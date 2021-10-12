from store.models import Cart
from django.utils import tree
from orders.views import checkout
from users.models import Profile
from django.contrib.auth import login
from django.http import request
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from .forms import UserLoginForm,CustomUserCreationForm,CheckAdress,UserNameForm
from django.contrib.auth.decorators import login_required
from orders.models import Order
from django.contrib.sessions.models import Session
from django.contrib import messages
# Create your views here.
def login_view(request):
    form=UserLoginForm()
  
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if request.session.get('cart',None):

                cart_pk=request.session['cart']
                print(f"cart antes:{cart_pk}")

                cart=Cart.objects.get(id=cart_pk)
                session=Session.objects.get(session_key=request.session.session_key)

                cart.session=session
                cart.save()
                
                # request.session["cart"]=cart
                # request.session.save()
                # print(f"sessão fim login {request.session.session_key}")
                # print(f"cart depois:{request.session['cart']}")

            return redirect('index')

            # Redirect to a success page.
            
        else:
            # Return an 'invalid login' error message.
            error="O email ou a palavra-chave estão incorretos"
            return render(request, 'registration/login.html',{'form':form,'error':error})
    else:
        
        return render(request, 'registration/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.method == "GET":

        return render(

            request, "registration/register.html",

            {"form": CustomUserCreationForm}

        )

    elif request.method == "POST":

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            profile=Profile(user=user)
            user.save()
            profile.save()
            
            login(request, user)

            return redirect("index")     
        else:
            return render(request, 'registration/register.html',{'form':form})

@login_required(login_url='login/')
def dashboard(request,x=1):

    
    if x==1:
        context={"flag":1, 'url':'/customer/ajax/account/'}
    elif x==2:
        orders=Order.objects.filter(user=request.user)

        context={"flag":2, 'url':'/customer/ajax/my-orders/', 'orders':orders}
    elif x==3:
    
        context={"flag":3, 'url':'/customer/ajax/my-adresses/'}
    elif x==4:
        context={"flag":4, 'url':'/customer/ajax/edit-account/'}

     
    return render(request,"users/dashboard.html",context)




#ajax

def ajax_account(request):
    orders=Order.objects.filter(user=request.user)

    context={
        'A_Aguardar_Pagamento': orders.filter(state="1").count(),
        'A_Processar':orders.filter(state="2").count(),
        'Enviadas':orders.filter(state="3").count(),
        'Concluidas':orders.filter(state="4").count(),
    }
    print(context)
    return render(request, 'ajax/account.html',context)


def ajax_my_orders(request):
    print("ajax, my orders")
    
    orders=Order.objects.filter(user=request.user)
    print(f'order: {orders}')
    return render(request, 'ajax/my-orders.html',{'orders':orders})


def ajax_adresses(request):
    print("ajax, ajax_account")


    return render(request, 'ajax/adresses.html')

def ajax_edit_account(request):
    user=request.user

    if request.method == "GET":
        form=UserNameForm(initial={"first_name":user.first_name,"last_name":user.last_name})

    elif request.method == "POST":
        form=UserNameForm(request.POST,instance=user)
        if form.is_valid():

            form.save()
            return redirect("dashboard-args",4)
        else:
            messages.add_message(request, messages.ERROR, 'Verifique os campos')

            return redirect("dashboard-args",4)


    return render(request, 'ajax/edit-account.html',{"form":form})

#edit 

def edit_adress(request,type=None):
    print("Aqui!!!!!!!!!!!!")



    if request.method == "GET":
        #aqui faço a decomposição da string para me dar os tres ultimos /url para idependetemente do localhost ou o protocolo...
        url=request.META['HTTP_REFERER']
        groups = url.split('/')
        url=groups[-1]+'/'+groups[-2]+'/'+groups[-3]+'/'
        print(url)
        if url == "/checkout/orders/":
            request.session['is_checking']=True

        print(request.session.get('is_checking',None))
        user=request.user

        if type=="normal":
            title="Endereço de envio"
            name_label="Destinatário"
            adress=request.user.profile.adress
            if adress:
                #duplicated code 1
                form=CheckAdress(initial={"receiver":adress.receiver,"street":adress.street,"postal_code":adress.postal_code,"city":adress.city,"district":adress.district,"contact":adress.contact,"nif":adress.nif})
            else:
                form=CheckAdress(initial={"receiver":user.first_name+" "+user.last_name})

        if type=="billing":
            title="Endereço de Faturação"
            name_label="Nome ou Empresa"
            adress=request.user.profile.adress_billing
            if adress:
                #duplicated code 2
                form=CheckAdress(initial={"receiver":adress.receiver,"street":adress.street,"postal_code":adress.postal_code,"city":adress.city,"district":adress.district,"contact":adress.contact,"nif":adress.nif} )
            else:
                form=CheckAdress(initial={"receiver":user.first_name+" "+user.last_name})
            
       

        return render(request, 'users/edit-adress.html',{'form':form, 'type':type, "title":title, "name_label":name_label})



    
    elif request.method == "POST":
        form=CheckAdress(request.POST)
        
        
        
        if form.is_valid():
            adress=form.save(commit=False)
            profile=Profile.objects.get(user=request.user)
            
            if type=='normal':
                profile.adress=adress
            elif type=='billing':   
                profile.adress_billing=adress
                
            
            adress.save()
            profile.save()
            # print(adress.instance.street)
            print("sucersso from form adress")

            return render(request, 'ajax/adresses.html',{'flag_sucess':True})
            # if request.session.get('is_checking',None):
            #     del request.session['is_checking']
            
            #     return redirect('checkout')
            # else:
            #     return redirect("dashboard-args",3)

        else:
            
            return render(request, 'users/edit-adress.html',{'form':form , 'type':type})

        
