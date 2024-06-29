from django.contrib import admin

# Register your models here.

from .models import User, Product,Cart,CartItem, Like,Order, OrderItem

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Like)
admin.site.register(Order)
admin.site.register(OrderItem)