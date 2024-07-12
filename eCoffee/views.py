from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
import logging
from .models import User,Product,CartItem,Cart,Like, Order, OrderItem
from .forms import ProductForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from decimal import Decimal
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from dotenv import load_dotenv
from django.conf import settings


load_dotenv()

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
endpoint_secret_success=os.getenv('SUCCESS_TRANSACTION_WEBHOOK_SECRET')


logging.basicConfig(level=logging.DEBUG)
# Create your views here.
footer_data = [
        ["Get to Know Us", "Careers", "Our Planet", "Investor Relations", "Press Releases", "Science"],
        ["Make Money with Us", "Sell on eCoffee", "Supply to eCoffee", "Become an Affiliate", "Protect & Build Your Brand", "Sell Handmade", "Advertise Your Products", "Independently Publish with Us", "Host a Hub"],
        ["Payment Products", "Rewards Mastercard", "Shop with Points", "Reload Your Balance", "Currency Converter", "Gift Cards", "Cash"],
        ["Let Us Help You", "Shipping Rates & Policies", "Prime Card Holders", "Returns Are Easy", "Manage your Content and Devices", "Recalls and Product Safety Alerts", "Customer Service"]
    ]
faq=[{"question":"How do I purchase coffee from eCoffee online?","answer":"To purchase coffee from eCoffee, simply browse our product selection, add your desired items to your cart, and proceed to checkout. You will need to create an account or log in if you already have one."},    
    {"question":"Does eCoffee offer discounts or promotional offers?","answer":"Currently, eCoffee does not offer discounts or promotional offers. We are exploring options to provide benefits to our patrons in the future. Stay tuned for updates on any upcoming promotions or special offers."},]


def index(request):
    # logging.debug('index got invoked::')
    for object in faq:
        logging.debug(f'{object["question"]}: {object["answer"]}')
    return render(request,'eCoffee/index.html',{'footer_data':footer_data,'faq':faq})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next_url = request.POST.get("next")  
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.username=='hon-admin':
                login(request, user)
                return redirect('main_dashboard')
            
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


from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime


def get_monthly_sales():       
    monthly_sales = Order.objects.annotate(month=TruncMonth('placed_order_at')).values('month').annotate(total=Sum('amount')).order_by('month')    
    
    return list(monthly_sales)

def sales_data(request):
    
    monthly_sales = get_monthly_sales()
    # logging.debug(f'monthly_sales::{monthly_sales}')
    return JsonResponse(monthly_sales, safe=False)

@user_passes_test(is_admin)
def main_dashboard(request):
    
    return render(request,'eCoffee/main_dashboard.html',{'dashboard':'eCoffee Admin DASHBOARD'})

@user_passes_test(is_admin)
def admin_products(request):    
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
        # logging.debug(f'selected_category::{selected_categories}')
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
            # logging.debug(f'index from FORM::{form_product_index}')
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
        # logging.debug(f'product_index::{product_index}')
        product_instance =None
        
        if product_index:
            product_instance=get_object_or_404(Product,pk=product_index)
            
        form=ProductForm(request.POST,request.FILES,instance = product_instance)
        # logging.debug(f'form inserted item::{form}')
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
        cart_item.quantity_purchased+=1
        cart_item.save()
        
        next_url=request.POST.get('next',reverse('products'))
        
        return HttpResponseRedirect(next_url)
    
    return render(request, 'eCoffee/products.html')

@login_required    
def cart_items(request):
    
    if request.user.is_authenticated:
        cart_user=Cart.objects.get(user=request.user)
        cart_items_user=cart_user.cart_items.all()
        
        cart_items=[{"product":object.product,"quantity":object.quantity_purchased,"sub_total":object.product.price*object.quantity_purchased } for object in cart_items_user]
        
        sum_sub_total=sum(object.product.price*object.quantity_purchased for object in cart_items_user)
        tax5=Decimal(0.05)*sum_sub_total
        tax7=Decimal(0.07)*sum_sub_total
        taxes=tax5+tax7
        total=sum_sub_total+taxes
        cart_length=request.POST.get('cart_length')

        return render(request,'eCoffee/cart.html',{'items':cart_items,'sum_sub_total':sum_sub_total,'tax5':tax5,'tax7':tax7,'taxes':taxes,'total':total}) 
    else:
        return redirect('login')
    
@login_required
def cart_delete_item(request,item_id):
    if request.method=="POST":
        my_cart=Cart.objects.get(user=request.user)
        my_cart_items=my_cart.cart_items.all()         
        # find the item (identified by item_id) in this my_cart_items
        item_to_delete=my_cart_items.filter(product=get_object_or_404(Product,pk=item_id))
      #   logging.debug(f'item_to_delete::{item_to_delete}')
        if item_to_delete:
            item_to_delete.delete()
            
        next_url=request.POST.get('three',reverse('cart_items'))
        return HttpResponseRedirect(next_url)
    
    return render(request,'eCoffee/cart_items.html')

@login_required
def update_cart_item(request,product_id):
    if request.method=="POST":
        cart=get_object_or_404(Cart,user=request.user)
        cart_item=get_object_or_404(CartItem,cart=cart,product=get_object_or_404(Product,pk=product_id))
        logging.debug(f'UPDATE cart_item::{cart_item}')
        if request.POST['modify_quantity']=="increase":
            if cart_item.quantity_purchased <10:
                cart_item.quantity_purchased +=1
        elif request.POST['modify_quantity']=="decrease":
            if cart_item.quantity_purchased >1:
                cart_item.quantity_purchased -=1
        
        cart_item.save()
        next_url=request.POST.get('three',reverse('cart_items'))
        
        return HttpResponseRedirect(next_url)
        
    # return redirect('cart_items')
    return render(request, 'eCoffee/cart_items.html')
 
@login_required
def product_details(request, product_id):
    
    product=get_object_or_404(Product,pk=product_id)
    user_cart=Cart.objects.get(user=request.user)
    cart_items=user_cart.cart_items.all()
   #  logging.debug(f'cart_items::{cart_items}')
    # logging.debug(f'all ids::{cart_item_ids}')
    existing_item= None
    for item in cart_items:
        if item.product==product:
            existing_item= item
            break
        
   #  logging.debug(f'existing item??::{existing_item}')
    return render(request, "eCoffee/product_details.html",{'product':product,'existing_item':existing_item})

def profile(request, user_id):
    logging.debug('Profile got triggered')
    
    my_cart = get_object_or_404(Cart, user__id=user_id)    
    orders_with_items = []
    profile= get_object_or_404(User, id=user_id)
    logging.debug(f'Who am I::{profile.username}')
    my_orders = Order.objects.filter(cart=my_cart, payment_status=True).order_by('-placed_order_at')
    
    for order in my_orders:
        order_items = []
       
        order_items_queryset = OrderItem.objects.filter(order=order)
        
        for item in order_items_queryset:
            product_details = {
                'description': item.product.description,
                'category': item.product.category,
                'price': item.product.price,
                'quantity_purchased': item.quantity_purchased,
                'photo_url': item.product.photo_url
            }
            order_items.append(product_details)
        
        orders_with_items.append({
            'order_id': order.id,
            'order_amount': order.amount,
            'placed_order_at': order.placed_order_at,
            'items': order_items
        })
    
    context = {
        'orders_with_items': orders_with_items,
        'profile':profile
    }
    
    return render(request, 'eCoffee/profile.html', context)

@login_required
def toggle_like(request, product_id):
   if request.method == "POST":
      product = get_object_or_404(Product, pk=product_id)
      liked = False
        
        # create a like instance
      like, created = Like.objects.get_or_create(user=request.user, product=product)
        
      if created:
         liked = True            
      else:
         like.delete()
            # logging.debug(f'No. Product {product_id} unliked by user {request.user}')
      logging.debug(f'{liked}. Product {product_id} liked by user {request.user}')
      return JsonResponse({'liked': liked})
    
   return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def create_checkout_session(request):
   if request.method == "POST":
        total = request.POST.get('total')
        cart_length = request.POST.get('cart_length')
        user_email=request.user.email
        try:           
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    "price_data": {
                        "currency": "cad",
                        "product_data": {
                            "name": f"{cart_length} items in cart"
                        },
                        "unit_amount": int(float(total) * 100),  
                    },
                    "quantity": 1
                }],
                mode="payment",
                cancel_url=f"{settings.BASE_URL}/failure_transaction",                
                success_url=f"{settings.BASE_URL}/success_transaction",               
                metadata={                    
                    "email": user_email 
                }
            )
            return redirect(session.url, code=303) 
         
        except stripe.error.StripeError as e:
            print(f"Stripe Error: {e}")
            logging.debug(f'Stripe Error Page: {e}')
            return render(request,'eCoffee/failure_transaction.html')
        
        except KeyError as e:
            logging.error(f'KeyError: {e} in payment_intent')
           
            return render(request,'eCoffee/failure_transaction.html')
         
        except Exception as e:
            print(f"Exception: {e}")
            logging.debug(f'cart_items: The transaction was not successful.{e}')
            
            return render(request,'eCoffee/failure_transaction.html')

   return redirect('cart_items') 

@csrf_exempt
def success_transaction(request):    
    return render(request,'eCoffee/success_transaction.html')  
    
@csrf_exempt
def failure_transaction(request):
    return render(request,'eCoffee/failure_transaction.html')

@csrf_exempt        
def stripe_webhook(request):
    logging.debug('Webhook called')
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        logging.debug(f'Error Stripe webhook::{e}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        logging.debug(f'payment_intent.payment_failed event received: {payment_intent}')
        logging.debug(f'ID: {payment_intent["id"]}')
        logging.debug(f'AMOUNT RECEIVED::{payment_intent["amount_received"]}')
        handle_payment_intent_failed(payment_intent)
        
        return HttpResponse(status=200)
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        logging.debug(f'SUCCESS payment_intent.succeeded event received: {payment_intent}')
        handle_payment_intent_succeeded(payment_intent)
        logging.debug('END Called handle_payment_intent_succeeded')
        return HttpResponse(status=200)
        
    else:
        logging.debug(f"Unhandled event type::{event['type']}")
        return JsonResponse({'success': True})
    
@csrf_exempt
def handle_payment_intent_succeeded(payment_intent):
    logging.debug('SUCCESS triggered handle_payment_intent_succeeded')
    try:
        logging.debug('SUCCESS Handling payment_intent.succeeded')
        payment_intent_id = payment_intent['id']
        amount = payment_intent['amount_received'] / 100.0  
       
        logging.debug(f'SUCCESS ID: {payment_intent["id"]}')
        logging.debug(f'SUCCESS AMOUNT RECEIVED::{amount}')  
        
       # Retrieve the user based on the payment_intent
        payment_method = payment_intent['payment_method']
        logging.debug(f'payment_method::{payment_method}')
        if payment_method:
            payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
            logging.debug(f'payment_method_object::{payment_method_obj}')
            payment_email = payment_method_obj['billing_details']['email']
            
            user=get_object_or_404(User,email=payment_email)
            cart=get_object_or_404(Cart,user=user)         
            
            
            order, created = Order.objects.get_or_create(
            payment_intent_id=payment_intent_id,
            defaults={'cart':cart,'amount': amount, 'payment_status': True})        

            if not created:
                order.payment_status = True
                order.amount = amount
                order.save()
                
            # use OrderItem
            cart_items = cart.cart_items.all()
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity_purchased=cart_item.quantity_purchased
                )
            # Clear the cart after the success transaction
            cart.cart_items.all().delete()
            
            logging.debug('SUCCESS: Cart items deleted')
            logging.debug(f'Order processed for successful payment: {order}')  

    except KeyError as e:
        logging.error(f'KeyError: {e} in payment_intent')
    
    except Exception as e:
        logging.error(f'Error handling payment intent success: {e}')
    

@csrf_exempt
def handle_payment_intent_failed(payment_intent):
    try:
        logging.debug('Handling payment_intent.payment_failed')
        payment_intent_id = payment_intent['id']
        logging.debug(f'ID FAILED::{payment_intent_id}')
        payment_email = payment_intent['last_payment_error']['payment_method']['billing_details']['email']
        
        user=get_object_or_404(User,email=payment_email)
        cart = Cart.objects.get(user=user)
        
        order, created = Order.objects.get_or_create(
            payment_intent_id=payment_intent_id,
            defaults={'cart': cart, 'payment_status': False}
        )
        logging.debug(f'order???:: {order}')
        logging.debug(f'created???:: {created}')

        if not created:
            order.payment_status = False
            order.save()

        logging.debug(f'Order processed for failed payment: {order}')
    except KeyError as e:
        logging.error(f'KeyError: {e} in payment_intent')
    
    except Exception as e:
        logging.error(f'Error handling payment intent failure: {e}')
    




    
    
    
