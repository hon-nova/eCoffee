from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
import logging
from .models import User

logging.basicConfig(level=logging.DEBUG)
# Create your views here.
footer_data = [
        ["Get to Know Us", "Careers", "Amazon and Our Planet", "Investor Relations", "Press Releases", "Amazon Science"],
        ["Make Money with Us", "Sell on Amazon", "Supply to Amazon", "Become an Affiliate", "Protect & Build Your Brand", "Sell on Amazon Handmade", "Advertise Your Products", "Independently Publish with Us", "Host an Amazon Hub"],
        ["Amazon Payment Products", "Amazon.ca Rewards Mastercard", "Shop with Points", "Reload Your Balance", "Amazon Currency Converter", "Gift Cards", "Amazon Cash"],
        ["Let Us Help You", "Shipping Rates & Policies", "Amazon Prime", "Returns Are Easy", "Manage your Content and Devices", "Recalls and Product Safety Alerts", "Customer Service"]
    ]
def index(request):
    logging.debug('index got invoked::')
    return render(request,'eCoffee/index.html',{'footer_data':footer_data})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "eCoffee/login_view.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "eCoffee/login_view.html")

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
    
