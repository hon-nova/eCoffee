from django.contrib import admin

# Register your models here.

from .models import User, Product,Cart,CartItem

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)