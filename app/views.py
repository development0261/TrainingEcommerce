from calendar import c
import email
from functools import total_ordering
from re import template
from unicodedata import category
from django.shortcuts import redirect, render,HttpResponse
from django.shortcuts import render
from django.views import View
from numpy import product
from .models import Customer,Product,Cart,OrderPlaced,Category,Wishlist
from .forms import CustomerRegistrationForm,ProfileForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

#category vice product display

class ProductView(View):
 def get(self,request): 
      # category = Category.objects.filter(category_name="Mobile")
      # print(category)
      Shirt = Product.objects.filter(category__category_name__contains="Shirt")
      Jeans = Product.objects.filter(category__category_name__contains="Jeans")
      Mobile = Product.objects.filter(category__category_name__contains="Mobile")
     
      Laptop = Product.objects.filter(category__category_name__contains="Laptop")
      return render(request, 'app/home.html',{'Shirt':Shirt,'Jeans':Jeans,'Mobile':Mobile,'Laptop':Laptop})

#check is product in cart
class ProductDetailView(View):
 def get(self,request,pk):
  product = Product.objects.get(pk=pk)
  in_cart = False
  in_list = False
  in_cart = Cart.objects.filter(Q(product=product.pk) & Q(user=request.user)).exists()
  in_list = Wishlist.objects.filter(Q(product=product.pk) & Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,'in_cart':in_cart,'in_list': in_list})

# @login_required
def product_detail(request,pk):
 #product = Product.objects.get(pk=pk)
 return render(request, 'app/productdetail.html')

#add to cart
@login_required(login_url='/login')
def add_to_cart(request):
      user = request.user 
      product_id = request.GET.get('prod_id')
      product  = Product.objects.get(pid=product_id)
      Cart(user=user,product=product).save()
      
      return redirect('/cart')

#show cart
# @login_required
def show_cart(request):
      if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user)

            amount = 0.0
            shipping_amount = 50.0
            total_amount = 0.0

            cart_product = [p for p in Cart.objects.all() if p.user == user]

            if cart_product:
                  for p in cart_product:
                        tempamount = (p.quantity * p.product.discounted_price)
                        amount += tempamount
                        total_amount  = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'total_amount':total_amount,'shipping_amount':shipping_amount,'amount':amount})

# @login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

# @login_required
def profile(request):
 return render(request, 'app/profile.html')

# @login_required
def address(request):
      address  = Customer.objects.filter(user=request.user)
      return render(request, 'app/address.html',{'address':address,'active':'btn-primary'})

# @login_required
def orders(request):
 user = request.user
 orders = OrderPlaced.objects.filter(user=user)
 return render(request, 'app/orders.html',{'orders':orders})

#login
def login_customer(request):
      if request.method=='POST':
         username = request.POST['username']
         password = request.POST['password']

         user = authenticate(request,username=username,password=password)

         if user is not None:
            login(request,user)
            # messages.success(request,("Successfully logged in"))
            return redirect("profile")
         else:
            messages.error(request,("User Name Or Password Is Incorrect"))
            return redirect("login")
      else:
          return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
      def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
      
      def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
              messages.success(request,'Registration Successfully')
              form.save()
              return redirect("home")
        return render(request, 'app/customerregistration.html',{'form':form})
      


 
def logout_customer(request):
      logout(request)
      return redirect("login")

def plus_cart(request):
      if request.method == 'GET':
            prod_id = request.GET['prod_id']
            user = request.user
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user) )
            c.quantity+=1
            c.save()
            amount = 0.0
            shipping_amount = 50.0
            
            cart_product  = [p for p in Cart.objects.all() if p.user == user]
            for p in cart_product:
                  tempamount = (p.quantity * p.product.discounted_price)
                  amount += tempamount
                  

            data = {
                  'quantity':c.quantity,
                  'amount':amount,
                  'totalamount':amount + shipping_amount
             }
            return JsonResponse(data)

def minus_cart(request):
      if request.method == 'GET':
            prod_id = request.GET['prod_id']
            user = request.user
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user) )
            c.quantity-=1
            c.save()
            amount = 0.0
            shipping_amount = 50.0
           
            cart_product  = [p for p in Cart.objects.all() if p.user == user]
            for p in cart_product:
                  tempamount = (p.quantity * p.product.discounted_price)
                  amount += tempamount

            if c.quantity == 0:
                  c.delete()
                  

            data = {
                  'quantity':c.quantity,
                  'amount':amount,
                  'totalamount':amount + shipping_amount
             }
            return JsonResponse(data)

def removecart(request):
      if request.method == 'GET':
            prod_id = request.GET['prod_id']
            user = request.user
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user) )
            c.delete()
            amount = 0.0
            shipping_amount = 50.0
            
            cart_product  = [p for p in Cart.objects.all() if p.user == user]
            for p in cart_product:
                  tempamount = (p.quantity * p.product.discounted_price)
                  amount += tempamount
                  

            data = {
                  'amount':amount,
                  'totalamount':amount + shipping_amount
             }
            return JsonResponse(data)

# @method_decorator(login_required,name='dispatch')
class ProfileView(View):
      def get(self,request):
            form = ProfileForm()
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
      def post(self,request):
            form = ProfileForm(request.POST)
            if form.is_valid():
                  user = request.user
                  name = form.cleaned_data['name']
                  locality = form.cleaned_data['locality']
                  city = form.cleaned_data['city']
                  state = form.cleaned_data['state']
                  zipcode = form.cleaned_data['zipcode']
                  customer = Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
                  customer.save()
                  messages.success(request,'Profile Created Successfully')
            return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

#checkout product and its total amount
def checkout(request):
      user = request.user
      address = Customer.objects.filter(user=user)
      cart_items  = Cart.objects.filter(user=user)
      amount = 0.0
      shipping_amount = 50.0
      totalamount = 0.0
      cart_product  = [p for p in Cart.objects.all() if p.user == user]
      if cart_product:
            for p in cart_product:
                  tempamount = (p.quantity * p.product.discounted_price)
                  amount += tempamount
            totalamount = amount + shipping_amount
      return render(request, 'app/checkout.html',{'address':address,'totalamount':totalamount,'cart_items':cart_items})

#order placed
def paymentdone(request):
      user = request.user
      custid = request.GET.get('custid')
      customer = Customer.objects.get(id=custid)
      cart = Cart.objects.filter(user=user)
      for c in cart:
            OrderPlaced(user=user,customer=customer,product=c.product,quantity= c.quantity,price=c.total_cost).save()
            c.delete()
      return redirect("orders")

def shirts(request,data=None):
       if data == None:
             Shirts = Product.objects.filter(category__category_name__contains="Shirt")
       elif data == 'Spiker' or data == 'levi':
             Shirts = Product.objects.filter(category__category_name__contains="Shirt").filter(brand=data)
       elif data == 'above':
             Shirts = Product.objects.filter(category__category_name__contains="Shirt").filter(discounted_price__gte=1000)
       elif data == 'below':
             Shirts = Product.objects.filter(category__category_name__contains="Shirt").filter(discounted_price__lte=700)
       return render(request,'app/topwears.html',{'Shirts':Shirts})

def wish_list(request):
      user = request.user
      wishlist = [p for p in Wishlist.objects.all() if p.user == user]
      return render(request,'app/wishlist.html',{'wishlist':wishlist})

def addto_wishlist(request):
      user = request.user 
      product_id = request.GET.get('pro_id')
      product  = Product.objects.get(pid=product_id)
      Wishlist(user=user,product=product).save() 
      return redirect('wishlist')

def jeans(request,data=None):
      if data == None:
            Jeans = Product.objects.filter(category__category_name__contains="Jeans")
      elif data == 'levi':
            Jeans = Product.objects.filter(category__category_name__contains="Jeans").filter(brand=data)
      elif data == 'below':
            Jeans = Product.objects.filter(category__category_name__contains="Jeans").filter(discounted_price__lte=700)
      elif data == 'above':
            Jeans = Product.objects.filter(category__category_name__contains="Jeans").filter(discounted_price__gt=1000)
      return render(request,'app/bottomwear.html',{'Jeans':Jeans})

def laptop(request,data=None):
      if data == None:
            Laptop = Product.objects.filter(category__category_name__contains="Laptop")
      elif data == 'Asus' or data == 'Acer':
            Laptop = Product.objects.filter(category__category_name__contains="Laptop").filter(brand=data)
      elif data == 'below':
            Laptop = Product.objects.filter(category__category_name__contains="Laptop").filter(discounted_price__lte=25000)
      elif data == 'above':
            Laptop = Product.objects.filter(category__category_name__contains="Laptop").filter(discounted_price__gt=25000)
      elif data == 'sort':
            Laptop = Product.objects.filter(category__category_name__contains="Laptop").order_by("discounted_price")
      return render(request,'app/laptop.html',{'Laptop':Laptop})

# @login_required
def mobile(request,data=None):
 if data == None:
       mobiles = Product.objects.filter(category__category_name__contains="Mobile")
 elif data == 'Samsung' or data == 'OnePluse' or data == 'Iphone':
       mobiles = Product.objects.filter(category__category_name__contains="Mobile").filter(brand=data)
 elif data == 'below':
       mobiles = Product.objects.filter(category__category_name__contains="Mobile").filter(discounted_price__lte=10000)
 elif data == 'above':
       mobiles = Product.objects.filter(category__category_name__contains="Mobile").filter(discounted_price__gt=10000)
 elif data == 'price':
       mobiles = Product.objects.filter(category__category_name__contains="Mobile").order_by("-discounted_price")    
 
 return render(request, 'app/mobile.html',{'mobiles':mobiles})  


            
