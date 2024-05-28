from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
import logging
from .models import User,Product,CartItem,Cart
from .forms import ProductForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

logging.basicConfig(level=logging.DEBUG)
# Create your views here.
footer_data = [
        ["Get to Know Us", "Careers", "Our Planet", "Investor Relations", "Press Releases", "Science"],
        ["Make Money with Us", "Sell on eCoffee", "Supply to eCoffee", "Become an Affiliate", "Protect & Build Your Brand", "Sell Handmade", "Advertise Your Products", "Independently Publish with Us", "Host a Hub"],
        ["Payment Products", "Rewards Mastercard", "Shop with Points", "Reload Your Balance", "Currency Converter", "Gift Cards", "Cash"],
        ["Let Us Help You", "Shipping Rates & Policies", "Prime Card Holders", "Returns Are Easy", "Manage your Content and Devices", "Recalls and Product Safety Alerts", "Customer Service"]
    ]
def index(request):
    logging.debug('index got invoked::')
    return render(request,'eCoffee/index.html',{'footer_data':footer_data})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next")  # Get the next URL from POST data
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return HttpResponseRedirect(next_url) 
            else:
                return redirect("index") 
        else:
            return render(request, "eCoffee/login_view.html", {
                "message": "Invalid username and/or password.",
                "next": next_url  
            })
    else:
        next_url = request.GET.get("next", "") 
        return render(request, "eCoffee/login_view.html", {"next": next_url})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "eCoffee/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "eCoffee/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "eCoffee/register.html")
    
    
def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def main_dashboard(request):
    
    return render(request,'eCoffee/main_dashboard.html',{'dashboard':'MY DASHBOARD CONTENT'})

@user_passes_test(is_admin)
def admin_products(request):    
    # products_count=len(Product.objects.all())
    categories_filtered=[object[0] for object in Product.CATEGORY_CHOICES]
    selected_category=request.GET.get('category','')
    # logging.debug(f'selected_category::{selected_category}')
    if selected_category:
        products=Product.objects.filter(category=selected_category)
        products=products.order_by('-created_at')
        products_count=len(products)
       
    else:
        products =Product.objects.all()        
        products=products.order_by('-created_at')
        products_count=len(products)
        paginator = Paginator(products, 10) 
        page = request.GET.get('page', 1)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)            
    # products_count=len(products)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = ProductForm(request.POST,request.FILES)        
            if form.is_valid():                
                product = form.save(commit=False)  
                product.save()    
                          
                return HttpResponseRedirect(reverse("admin_products"))
        else:
            return redirect('login')    
    else:
        form = ProductForm()        
    
    return render(request, "eCoffee/admin_products.html", {"form": form,'products':products,'categories':categories_filtered,'selected_category':selected_category,'products_count':products_count})
    

def home_products(request):
    
    categories_filtered=[object[0] for object in Product.CATEGORY_CHOICES]
    selected_categories=request.GET.getlist('category')
    
    if selected_categories:
        products=Product.objects.filter(category__in=selected_categories).order_by('-created_at')
        logging.debug(f'selected_category::{selected_categories}')
        # logging.debug(f'products associated selected_category::{products}')
        products_count=len(products)
    else:
        products=Product.objects.all().order_by('-created_at')    
        products_count=len(products)
    
    paginator = Paginator(products, 12) 
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)   
    return render(request,'eCoffee/home_products.html',{'products':products,'footer_data':footer_data,'categories':categories_filtered,'selected_categories':selected_categories,'products_count':products_count})

@user_passes_test(is_admin)
def admin_users(request):
    users=User.objects.exclude(username='hon-admin')
    return render(request,'eCoffee/admin_users.html',{'users':users})

@user_passes_test(is_admin)
def delete_product(request):
    if request.method=="POST":
        form_product_index=request.POST.get('product_index')
        try:
            form_product_index=int(form_product_index)
            logging.debug(f'index from FORM::{form_product_index}')
        except(ValueError):
            return redirect('admin_products')       

        products= Product.objects.all()
        products = products.order_by('-created_at')
        
        if form_product_index < len(products):
            product_to_delete=products[form_product_index]
            product_to_delete.delete()
        return redirect('admin_products')    
    return render(request,'eCoffee/admin_products.html',{"products":products})

@user_passes_test(is_admin)
def get_product(request,product_id):    
    product=get_object_or_404(Product,pk=product_id)    
   
    data = {
    'id':product.id,
    'description': product.description,
    'category': product.category,
    'price': product.price,
    'quantity':product.quantity,
    'photo_url': product.photo_url,
    }
    # logging.debug(f'data::{data}')
    return JsonResponse(data)

@user_passes_test(is_admin)
def save_product(request):  
    
    products=Product.objects.all().order_by('-created_at')    
    
    if request.method == 'POST':
        product_index=request.POST.get('product_index','')
        logging.debug(f'product_index::{product_index}')
        product_instance =None
        
        if product_index:
            product_instance=get_object_or_404(Product,pk=product_index)
            
        form=ProductForm(request.POST,request.FILES,instance = product_instance)
        logging.debug(f'form inserted item::{form}')
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form=ProductForm()
    return render(request,'eCoffee/admin_products.html',{'form':form,'products':products})

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        cart, created=Cart.objects.get_or_create(user=request.user)
        cart_item, created=CartItem.objects.get_or_create(cart=cart,product=product)
        
        cart_item.save()
        
        return HttpResponseRedirect(reverse('products'))
    
    # return redirect('products')
    # return HttpResponseRedirect(reverse('products'))
    return render(request, 'eCoffee/products.html')
    
def cart_items(request):
    if request.user.is_authenticated:
        cart_user=CartItem.objects.filter(user=request.user)
        cart_items=cart_user.user_products.all()
        return render(request,'eCoffee/cart.html',{'items':cart_items})       
        
        
    else:
        return redirect('login')
    
    
    
