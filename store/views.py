from django.shortcuts import render  ,redirect,get_object_or_404
from django.views import View
from  .models import product,Customer,Cart,OrderPlaced
from django.db.models import Count
from .forms import CustomerRegisterationForm  ,CustomerForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
    return render(request,'home.html')
#categories page ,class based view

class category(View):
    def get(self,request,val):
        products=product.objects.filter(category=val) #fetch data of category from models
        return render(request,'category.html',locals())
#product details page

class ProductDetail(View):
    def get(self,request,pk):
         products=product.objects.get(pk=pk) #get items or categories using primary key :id 
         return render(request ,'product_detail.html',locals())
     
# about page 
def about(request):
    return render(request,'about.html')

#contact page 
def contact(request):
    return render(request,'contact.html')     

#authentication  class based function view
class CustomerRegistration(View):
    def get(self,request):
         form=CustomerRegisterationForm()
         return render(request ,'Registration.html',locals())
     #check validity of form and register user
    def post (self,request):
         form=CustomerRegisterationForm(request.POST)
         if form.is_valid():
             form.save()
             messages.success(request,'Registration Successful')
             return redirect('login') 
         else:
             messages.error(request,'Registration Failed')    
             return render(request,'Registration.html',locals())



# profile section 

class profile(View):
    def get(self,request):
        Form=CustomerForm()
        return render(request ,'profile.html',locals())
    def post(self,request):
        Form=CustomerForm(request.POST)
        if Form.is_valid():
            user=request.user
            name=Form.cleaned_data['name']
            locality=Form.cleaned_data['locality']
            city=Form.cleaned_data['city']
            mobile=Form.cleaned_data['mobile']
            zipcode=Form.cleaned_data['zipcode']
            state=Form.cleaned_data['state']
            reg=Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,zipcode=zipcode,state=state)
            reg.save()
             
             
            messages.success(request,'profile added Successful')
            return redirect('checkout') 
        else:
             messages.error(request,'update Failed')    
             return render(request,'profile.html',locals())



# adress section 

class adress(View):
    def get(self,request):
        addresses = Customer.objects.filter(user=request.user)
        return render(request ,'adress.html',locals())
    def post(self,request):
         return render(request ,'adress.html',locals())
        
        
        
# updateadress


class update(View):
    def get(self, request, pk):
        address = get_object_or_404(Customer, pk=pk, user=request.user)
        form = CustomerForm(instance=address)
        return render(request, 'updateadress.html', {'form': form, 'address': address})

    def post(self, request, pk):
        address = get_object_or_404(Customer, pk=pk, user=request.user)
        form = CustomerForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated successfully!")
            return redirect('adress')  # Redirect to address page
        else:
            messages.error(request, "Update failed! Please correct the errors below.")
        return render(request, 'updateadress.html', {'form': form, 'address': address})



# logout
def custom_logout(request):
    logout(request)
    return redirect('login')  


# cart section

@login_required(login_url='/accounts/login/')
def add_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')

    if not product_id:
        return redirect('/')

    try:
        prod = product.objects.get(id=product_id)
    except product.DoesNotExist:
        return redirect('/')

    Cart.objects.create(user=user, product=prod)
    return redirect('/cart')

# show cart
def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart)
    shipping_amount = 40 if cart else 0
    totalamount = amount + shipping_amount
    return render(request, 'cart.html', {
        'cart': cart,
        'amount': amount,
        'totalamount': totalamount,
    })


# plus button

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=user))
        if cart_items.exists():
            # Keep only one record
            c = cart_items.first()

            # Merge duplicates (only once, before increment)
            if cart_items.count() > 1:
                for dup in cart_items.exclude(id=c.id):
                    c.quantity += dup.quantity
                    dup.delete()

            # Now safely increment by 1
            c.quantity += 1
            c.save()

        # Recalculate totals
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity if cart_items.exists() else 0,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)

# minus button


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user

        # Get all cart entries for this product & user
        cart_items = Cart.objects.filter(Q(product=prod_id) & Q(user=user))

        if cart_items.exists():
            # Keep one record safely
            c = cart_items.first()

            # Merge duplicates (only once, before decreasing)
            if cart_items.count() > 1:
                for dup in cart_items.exclude(id=c.id):
                    c.quantity += dup.quantity
                    dup.delete()

            # Decrease quantity by 1 (but not below zero)
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()  # remove item completely when quantity is 1

        # Recalculate totals
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40

        data = {
            'quantity': c.quantity if cart_items.exists() and c.id else 0,
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)
    # remove button

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        user = request.user
        Cart.objects.filter(Q(product=prod_id) & Q(user=user)).delete()
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40  # shipping cost

        data = {
            'amount': amount,
            'totalamount': totalamount
        }

        return JsonResponse(data)





# checkout

@login_required
def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = sum(item.quantity * item.product.discounted_price for item in cart_items)
    totalamount = amount + 40 if amount > 0 else 0

    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'amount': amount,
        'totalamount': totalamount,
    }
    return render(request, 'checkout.html', context)
# placed order

@login_required
def place_order(request):
    if request.method == "POST":
        address_id = request.POST.get("selected_address")
        if not address_id:
            messages.warning(request, "⚠️ Please select a delivery address!")
            return redirect('checkout')

        customer = Customer.objects.get(id=address_id)
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items:
            messages.warning(request, "⚠️ Your cart is empty!")
            return redirect('cart')

        # Create OrderPlaced entries
        for item in cart_items:
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                status='Accepted',  # initial status
            )

        # Clear cart
        cart_items.delete()

        messages.success(request, "✅ Your order has been placed!")
        return redirect('orders') 

    return redirect('checkout')

# orders tracking
@login_required
def orders(request):
    user = request.user
    order_items = OrderPlaced.objects.filter(user=user).order_by('-ordered_date')
    return render(request, 'orders.html', {'order_items': order_items})

