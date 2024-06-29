from django.contrib import admin

# Register your models here.

from .models import User, Product,Cart,CartItem, Like,Order, OrderItem
from .forms import OrderForm

class OrderAdmin(admin.ModelAdmin):
   
   form = OrderForm
   list_display = ('cart', 'payment_status', 'placed_order_at', 'amount')
   fields = ('cart', 'payment_status', 'placed_order_at', 'payment_intent_id', 'amount')

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Like)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)