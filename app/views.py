from django.conf import settings
from django.shortcuts import render, redirect
from django.test import Client
from django.views import View
from .models import Customer, Payment, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm, SearchForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
import razorpay

# PRODUCT VIEW
class ProductView(View):
    def get(self, request):
        totalitem = 0
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        mentopwears = Product.objects.filter(category='MT')
        menbottomwears = Product.objects.filter(category='MB')
        womentopwears = Product.objects.filter(category='WT')
        womenbottomwears = Product.objects.filter(category='WB')
        boyswears = Product.objects.filter(category='B')
        girlswears = Product.objects.filter(category='G')
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
        
        return render(request, 'app/home.html', {'mentopwears':mentopwears,'menbottomwears':menbottomwears, 'womentopwears':womentopwears, 'womenbottomwears':womenbottomwears, 'boyswears':boyswears, 'girlswears':girlswears, 'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, 'totalitem':totalitem,})


# PRODUCT DETAILS VIEW
class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
         item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})


#ADD TO CART VIEW
@login_required
def add_to_cart(request):
   user = request.user
   product_id = request.GET.get('prod_id')
   product= Product.objects.get(id=product_id)
   Cart(user=user, product=product).save()
   return redirect('/cart')


#SHOW CART VIEW
@login_required
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
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
            total_amount = amount + shipping_amount
         return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'total_amount':total_amount})
      else:
         return render(request, 'app/emptycart.html')


#PLUS BUTTON VIEW
@login_required
def plus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print(prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      amount = 0.0
      shipping_amount = 50.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount

      data={
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
         }
      return JsonResponse(data)


#MINUS BUTTON VIEW
@login_required
def minus_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      print(prod_id)
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      if c.quantity <= 1:
         c.delete()  # Remove item if quantity is zero or less
                
      c.quantity-=1
      c.save()
      amount = 0.0
      shipping_amount = 50.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount
      if c.quantity < 1:
         c.delete() 
         

      data={
            'quantity': c.quantity,
            'amount': amount,
            'total_amount': amount + shipping_amount
         }
      return JsonResponse(data)


# REMOVE CART BUTTON VIEW
@login_required
def remove_cart(request):
   if request.method == 'GET':
      prod_id = request.GET['prod_id']
      c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
      c.delete()      
      amount = 0.0
      shipping_amount = 50.0
      cart_product = [p for p in Cart.objects.all() if p.user == request.user]
      
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount
         total_amount = amount

      data={
            'amount':amount,
            'total_amount': amount + shipping_amount
         }
      return JsonResponse(data)


# LOGIN VIEW
@login_required
def buy_now(request):
 
 return render(request, 'app/buynow.html')


# MOBILE VIEW
def mobile(request, data=None):
 if data == None:
    mobiles = Product.objects.filter(category='M')

 elif data == 'Redmi' or data == 'Oneplus' or data == 'Sony' or data == 'Realme' or data == 'Asus'or data == 'Samsung' or data =='Apple':
    mobiles = Product.objects.filter(category='M').filter(brand=data)
 
 elif data == 'Samsung':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)

 elif data == 'Below':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 
 elif data == 'Above':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

 return render(request, 'app/mobile.html', {'mobiles':mobiles})


# LAPTOP VIEW
def laptop(request, data=None):
 if data == None:
    laptops = Product.objects.filter(category='L')

 elif data == 'Redmi' or data == 'MacBook' or data == 'hp' or data == 'dell' or data == 'Lenovo':
    laptops = Product.objects.filter(category='L').filter(brand=data)
 
 elif data == 'Below':
    laptops = Product.objects.filter(category='L').filter(discounted_price__lt=10000)
 
 elif data == 'Above':
    laptops = Product.objects.filter(category='L').filter(discounted_price__gt=10000)

 return render(request, 'app/laptop.html', {'laptops':laptops})


#mentopwear
def mentopwear(request, data=None):
   if data == None:
      mentopwears = Product.objects.filter(category='MT')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      mentopwears = Product.objects.filter(category='MT').filter(brand=data)
   elif data == 'Below':
      mentopwears = Product.objects.filter(category='MT').filter(discounted_price__lt=10000)
   elif data == 'Above':
      mentopwears = Product.objects.filter(category='MT').filter(discounted_price__gt=30000)
   return render(request, 'app/mentopwear.html', {'mentopwears':mentopwears})


#menbottomwear
def menbottomwear(request, data=None):
   if data == None:
      menbottomwears = Product.objects.filter(category='MB')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      menbottomwears = Product.objects.filter(category='MB').filter(brand=data)
   elif data == 'Below':
      menbottomwears = Product.objects.filter(category='MB').filter(discounted_price__lt=10000)
   elif data == 'Above':
      menbottomwears = Product.objects.filter(category='MB').filter(discounted_price__gt=30000)
   return render(request, 'app/menbottomwear.html', {'menbottomwears':menbottomwears})

# womantop
def womentopwear(request, data=None):
   if data == None:
      womentopwears = Product.objects.filter(category='WT')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      womentopwears = Product.objects.filter(category='WT').filter(brand=data)
   elif data == 'Below':
      womentopwears = Product.objects.filter(category='WT').filter(discounted_price__lt=10000)
   elif data == 'Above':
      womentopwears = Product.objects.filter(category='WT').filter(discounted_price__gt=30000)
   return render(request, 'app/womentopwear.html', {'womentopwears':womentopwears})


# womanbottom
def womenbottomwear(request, data=None):
   if data == None:
      womenbottomwears = Product.objects.filter(category='WB')
   elif data == 'Denim' or data == 'Mufti' or data == 'BeingHuman' or data == 'JackJohn':
      womenbottomwears = Product.objects.filter(category='WB').filter(brand=data)
   elif data == 'Below':
      womenbottomwears = Product.objects.filter(category='WB').filter(discounted_price__lt=3000)
   elif data == 'Above':
      womenbottomwears = Product.objects.filter(category='WB').filter(discounted_price__gt=10000)
   return render(request, 'app/womenbottomwear.html', {'womenbottomwears':womenbottomwears})


# CHECKOUT DONE VIEW
@login_required
def checkout(request):
   user = request.user
   add = Customer.objects.filter(user=user)
   cart_items = Cart.objects.filter(user=user)
   amount = 0.0
   shipping_amount = 50.0
   total_amount = 0.0
   razorpayamount = 0
   order_id = ""
   cart_product = [p for p in Cart.objects.all() if p.user == request.user]
   if cart_product: 
      for p in cart_product:
         temp_amount = (p.quantity * p.product.discounted_price)
         amount += temp_amount
      total_amount = amount + shipping_amount
      razorpayamount = int(total_amount * 100)

      client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
      data = {"amount": razorpayamount, "currency": "INR", "receipt":"order_rectid_12"}
      payment_respones = client.order.create(data=data)
      print(payment_respones)

      #{'amount': 40000, 'amount_due': 40000, 'amount_paid': 0, 'attempts': 0, 'created_at': 1720508019, 'currency': 'INR', 'entity': 'order', 'id': 'order_OWRRj6NYs9BCdi', 'notes': [], 'offer_id': None, 'receipt': 'order_rectid_12', 'status': 'created'}
      order_id = payment_respones['id']
      order_status = payment_respones['status']

      if order_status == "created":
         payment = Payment(
            user=user,
            amount = total_amount,
            razorpay_order_id=order_id,
            razorpay_payment_status = order_status,
         )
         payment.save()
   return render(request, 'app/checkout.html', {'add':add, 'razorpayamount':razorpayamount, 'amount':amount, 'cart_items':cart_items, 'order_id': order_id,'total_amount': total_amount})



# PAYMENT DONE VIEW
@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user

    try:
        customer = Customer.objects.get(id=cust_id)
    except Customer.DoesNotExist:
        return redirect('checkout')  # Redirect to checkout if the customer is not found

    try:
        payment = Payment.objects.get(razorpay_order_id=order_id)
    except Payment.DoesNotExist:
        return redirect('checkout')  # Redirect to checkout if the payment is not found

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    cart_items = Cart.objects.filter(user=user)
    for c in cart_items:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()

    return redirect("orders")
#order Page 
@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
           totalitem = len(Cart.objects.filter(user=request.user))
    # Calculate total price for each order item
    orders_with_total = []
    for order in order_placed:
        total_price = order.product.discounted_price * order.quantity
        orders_with_total.append({
            'order': order,
            'total_price': total_price,
        })

    return render(request, 'app/orders.html', {'orders_with_total': orders_with_total,'totalitem':totalitem})
# CUSTOMER REGISTRATION VIEW
class CustomerRegistrationView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form,})
    
    def post(self, request):
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages .success(request, 'Congratulations..! Registered Successfully.')
            form.save()
      
        return render(request, 'app/customerregistration.html', {'form':form})


# PROFILE VIEW
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
   
   def get(self, request):

      form = CustomerProfileForm()
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})
   
   def post(self, request):
      totalitem = 0
      form = CustomerProfileForm(request.POST)  
      if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name']
         locality = form.cleaned_data['locality']
         city = form.cleaned_data['city']
         state = form.cleaned_data['state']
         zipcode = form.cleaned_data['zipcode']
         reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
         reg.save()
         messages.success(request, 'Congratulations! Profile Updated Successfully')
         
      
      return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary','totalitem':totalitem})


# ADDRESS VIEW
def address(request):                                                                                              
   
   add = Customer.objects.filter(user=request.user)

   return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})


def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Product.objects.filter(title__icontains=query) | Product.objects.filter(description__icontains=query)

    return render(request, 'app/search.html', {'form': form, 'query': query, 'results': results})