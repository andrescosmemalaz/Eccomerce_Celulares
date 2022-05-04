from itertools import product
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Carrito, Costumer, PedidoRealizado, Product
from app.forms import CustomerRegistrationForm
from django.contrib import  messages
from .forms import CostumerProfileform
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#     return render(request, 'app/home.html')

class ProductView(View):
    def get(self, request):
     totalitem = 0
     celulares = Product.objects.filter(category = 'C')
     laptops = Product.objects.filter(category = 'L')
     tablets = Product.objects.filter(category = 'T')
     games = Product.objects.filter(category = 'G')
     computadors = Product.objects.filter(category = 'Pc')
     fundas = Product.objects.filter(category = 'F')
     micas = Product.objects.filter(category = 'M')
     audifonos = Product.objects.filter(category = 'A')
     tarjets = Product.objects.filter(category = 'T')
     otros = Product.objects.filter(category = 'B')
     repuestos = Product.objects.filter(category = 'R')
     if request.user.is_authenticated:
       totalitem = len(Carrito.objects.filter(user=request.user))
     return render(request, 'app/home.html', 
    {'celulares':celulares,'laptops':laptops,'tablets':tablets,
    'games':games,'computadors':computadors,'fundas':fundas,'micas':micas,
    'audifonos':audifonos,'tarjets':tarjets,'otros':otros,'repuestos':repuestos, 'totalitem': totalitem})
     

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
     item_already_in_cart = Carrito.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()   
  return render(request, 'app/productdetail.html',
  {'product':product, 'item_already_in_cart':item_already_in_cart})
    
@login_required
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Carrito(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Carrito.objects.filter(user=user)
    # print(cart)
    cantidad = 0.0
    monto_de_envio = 70.0
    cantidadtotal = 0.0
    cart_product = [p for p in Carrito.objects.all() if p.user == user]
    # print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.selling_price)
        cantidad += tempamount
        cantidadtotal = cantidad + monto_de_envio
      return render(request, 'app/addtocart.html', {'carts':cart, 'cantidadtotal':cantidadtotal, 'cantidad':cantidad})
    else:
      return render(request, 'app/emptycart.html')

def plus_cart(request):
  if request.method == 'GET':   
    prod_id = request.GET['prod_id']
    print(prod_id)
    c = Carrito.objects.get(Q(product=prod_id) & Q(user=request.
    user))
    c.quantity+=1
    c.save() 
    cantidad = 0.0
    monto_de_envio  = 70.0
    cart_product = [p for p in Carrito.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.selling_price)
      cantidad += tempamount
       
    data = {
      'quantity': c.quantity,
      'cantidad':cantidad,
      'cantidadtotal': cantidad + monto_de_envio
      }
    return JsonResponse(data)

def minus_cart(request):
  if request.method == 'GET':   
    prod_id = request.GET['prod_id']
    print(prod_id)
    c = Carrito.objects.get(Q(product=prod_id) & Q(user=request.
    user))
    c.quantity-=1
    c.save() 
    cantidad = 0.0
    monto_de_envio  = 70.0
    cart_product = [p for p in Carrito.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.selling_price)
      cantidad += tempamount
      # cantidadtotal = cantidad + monto_de_envio
       
    data = {
      'quantity': c.quantity,
      'cantidad':cantidad,
      'cantidadtotal': cantidad + monto_de_envio
      }
    return JsonResponse(data)


def remove_cart(request):
  if request.method == 'GET':   
    prod_id = request.GET['prod_id']
    # print(prod_id)
    c = Carrito.objects.get(Q(product=prod_id) & Q(user=request.
    user))
    c.delete() 
    cantidad = 0.0
    monto_de_envio  = 70.0
    cart_product = [p for p in Carrito.objects.all() if p.user == request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.selling_price)
      cantidad += tempamount
      
    data = {
      'cantidad':cantidad,
      'cantidadtotal':cantidad + monto_de_envio
      }
    return JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@login_required
def address(request):
 add = Costumer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'add':add, 
 'active':'btn-primary'})

@login_required
def orders(request):
 op = PedidoRealizado.objects.filter(user = request.user)
 return render(request, 'app/orders.html', {'order_placed':op})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data == None:
  celulares = Product.objects.filter(category='C')
 elif data == 'SAMSUNG' or data == 'Huawei':
  celulares = Product.objects.filter(category='C').filter(brand=data)
 elif data == 'Xiaomi' or data == 'MOTOROLA':
  celulares = Product.objects.filter(category='C').filter(brand=data)  
 elif data =='LG' or data == 'Apple':
  celulares = Product.objects.filter(category='C').filter(brand=data)
 elif data == 'Abajo':
  celulares = Product.objects.filter(category='C').filter(selling_price__lt=600)
 elif data == 'Sobre':
  celulares = Product.objects.filter(category='C').filter(selling_price__gt=600)
 return render(request, 'app/mobile.html',{'celulares':celulares})


# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
     form = CustomerRegistrationForm()
     return render(request, 'app/customerregistration.html', {'form':form})
 
    def post(self, request):
     form = CustomerRegistrationForm(request.POST)
     if form.is_valid():
      messages.success(request, 'Felicidades!! Registro Actualizado C orrectamente')
      form.save()
     return render(request, 'app/customerregistration.html', 
     {'form':form})

@login_required
def checkout(request):
 user = request.user
 add = Costumer.objects.filter(user=user)
 cart_items = Carrito.objects.filter(user = user)
 cantidad = 0.0
 monto_envio = 70.0
 cantidadtotal = 0.0
 cart_product = [p for p in Carrito.objects.all() if p.user == request.user]
 if cart_product:
   for p in cart_product:
     tempamount = (p.quantity * p.product.selling_price)
     cantidad += tempamount
   cantidadtotal = cantidad + monto_envio  
 return render(request, 'app/checkout.html', {'add':add, 'cantidadtotal':cantidadtotal, 'cart_items':cart_items})


@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid')
  customer = Costumer.objects.get(id = custid)
  cart = Carrito.objects.filter(user=request.user)
  for c in cart:
    PedidoRealizado(user=user, customer = customer, product=c.product,
    quantity=c.quantity).save()
    c.delete()
  return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
      form = CostumerProfileform()
      return render(request, 'app/profile.html', {'form':form,
      'activate':'btn-primary'})
    
    def post(self, request):
      form = CostumerProfileform(request.POST)
      if form.is_valid():
        usr = request.user
        name= form.cleaned_data['name']
        locality= form.cleaned_data['locality']
        city= form.cleaned_data['city']
        state= form.cleaned_data['state']
        zipcode= form.cleaned_data['zipcode']
        reg = Costumer(user = usr, name=name, locality= locality, city=city, 
        state=state, zipcode=zipcode)
        reg.save()
        messages.success(request, 'Felicidades!! Perfil Actualizado Satisfactoriamente')
      return render(request, 'app/profile.html', {'form':form, 
      'activate':'btn-primary'})    

