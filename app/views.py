from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from . forms import SignUpForm, LoginFrom, CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import OrderPlaced, Product, Customer, Cart

def home(request):
    men_wear = Product.objects.all().filter(category='MW')
    cameras = Product.objects.all().filter(category='C')
    home_appliances = Product.objects.all().filter(category='HP')
    deal_day = Product.objects.order_by('?')
    return render(request, 'app/home.html', {'men_wear':men_wear, 'cameras':cameras, 'home_appliances':home_appliances, 'deal_day':deal_day})

def product_detail(request, pk):
    prod_detail = Product.objects.get(pk=pk)
    return render(request, 'app/productdetail.html', {'prod_detail':prod_detail})

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        show_cart = Cart.objects.filter(user=user)
        # total amount
        amount = 0.0
        shipping = 90.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount+=tempamount
                total = amount+shipping
        return render(request, 'app/addtocart.html', {'show_cart':show_cart, 'total':total, 'amount':amount})  
    return redirect('/login/')

def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        crt = Cart(user=user, product=product)
        crt.save()
        return redirect('/cart/')
    return redirect('/login/')

def plus_cart(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity+=1
            c.save()
            amount = 0.0
            shipping = 90.0
            total = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user==request.user]
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount+=tempamount
                total = amount+shipping
                
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'total':total
            }
            return JsonResponse(data)
    return redirect('/login/')

def minus_cart(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.quantity-=1
            c.save()
            amount = 0.0
            shipping = 90.0
            total = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user==request.user]
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount+=tempamount
                total = amount+shipping
                
            data = {
                'quantity':c.quantity,
                'amount':amount,
                'total':total
            }
            return JsonResponse(data)
    return redirect('/login/')

def remove_cart(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            prod_id = request.GET['prod_id']
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.delete()
            amount = 0.0
            shipping = 90.0
            total = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user==request.user]
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount+=tempamount
                total = amount+shipping
                
            data = {
                'amount':amount,
                'total':total
            }
            return JsonResponse(data)
    return redirect('/login/')

def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping = 90.0
        total = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity*p.product.discounted_price)
                amount+=tempamount
            total = amount+shipping
        return render(request, 'app/checkout.html', {'total':total, 'add':add, 'cart_items':cart_items})
    return redirect('/login/')


def orders(request):
    if request.user.is_authenticated:
        user = request.user
        orders = OrderPlaced.objects.filter(user=user)
        return render(request, 'app/orders.html', {'orders':orders})
    return redirect('/login/')

def payment_done(request):
    if request.user.is_authenticated:
        user = request.user
        if request.GET.get('custid'):
            custid = request.GET.get('custid')
            customer = Customer.objects.get(id=custid)
            cart = Cart.objects.filter(user=user)
            for c in cart:
                OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
                c.delete()
            return redirect("orders")
        else:
            messages.info(request, 'Address Not Selected!')
            return redirect('orders')
    return redirect('/login/')


def product_fltr(request, data):
    tmplt = 'app/men_wear.html'
    if data == 'mw' or data == 'puma' or data == 'addi':
        if data == 'addi':
            filter_prod = Product.objects.filter(category='MW').filter(brand='Addi')
        elif data == 'puma':
            filter_prod = Product.objects.all().filter(category='MW').filter(brand='Puma')
        else:
            filter_prod = Product.objects.all().filter(category='MW')

    elif data == 'ha' or data == 'samsung' or data == 'nokia':
        tmplt = 'app/home_appliances.html'
        if data == 'samsung':
            filter_prod = Product.objects.filter(category='HP').filter(brand='Samsung')
        elif data == 'nokia':
            filter_prod = Product.objects.filter(category='HP').filter(brand='Nokia')
        else:
            filter_prod = Product.objects.all().filter(category='HP')

    elif data == 'c' or data == 'nicon' or data == 'canon':
        tmplt = 'app/camera.html'
        if data == 'canon':
            filter_prod = Product.objects.filter(category='C').filter(brand='Canon')
        elif data == 'nicon':
            filter_prod = Product.objects.all().filter(category='C').filter(brand='Nicon')
        else:
            filter_prod = Product.objects.all().filter(category='C')
    return render(request, tmplt , {'filter_prod':filter_prod})


class Profile(TemplateView):
    def get(self, request):
        form = CustomerForm()
        return render(request, 'app/profile.html', {'form':form,  'active':'btn-secondary'})

    def post(self, request):
        form = CustomerForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            obj = Customer(user=request.user, name=name, locality=locality, city=city, zipcode=zipcode, state=state)
            obj.save()
            messages.success(request, 'Your data is added!!!')
        return render(request, 'app/profile.html', {'form':form})


def address(request):
    if request.user.is_authenticated:
        obj = Customer.objects.filter(user=request.user)
        return render(request, 'app/address.html', {'obj':obj,  'active':'btn-secondary'})
    return redirect('/login/')


def change_password(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password Changed!!!')
                return redirect('/changepassword/')
            else:
                return redirect('/changepassword/')
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'app/changepassword.html', {'form':form})
    else:
        return redirect('/login/')


def LoginView(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginFrom(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Successfully Logedin!!!')
                    return redirect('/')
            else:
                return redirect('/login/')
        else:
            form = LoginFrom()
        return render(request, 'app/log_in.html', {'form':form})
    else:
        return redirect('/')


# customer registration
def SignUpView(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully Register!!!')
        else:
            form = SignUpForm()
        return render(request, 'app/sign_up.html', {'form':form})
    return redirect('/')