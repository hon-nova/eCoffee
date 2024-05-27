from django.urls import path,include

from . import views
urlpatterns =[
   path('',views.index,name="index"),
   path("login", views.login_view, name="login"),
   path("logout", views.logout_view, name="logout"),
   path("register", views.register, name="register"),
   path('coffee_admin',views.main_dashboard,name="main_dashboard"),
   path("coffee_admin/products",views.admin_products,name="admin_products"),
   path("get_product/<int:product_id>",views.get_product,name="get_product"),
   path('coffee_admin/users',views.admin_users,name='admin_users'),  
   path('home_products',views.home_products,name="products"),
   path('delete_product',views.delete_product,name="delete_product"),
   path('save_product',views.save_product,name="save_product"),
   path('cart_items',views.cart_items,name="cart_items"),
   path('cart/<int:product_id>',views.add_to_cart,name="add_to_cart")
   
]