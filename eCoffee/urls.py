from django.urls import path,include

from . import views
urlpatterns =[
   path('',views.index,name="index"),
   path("accounts/login/", views.login_view, name="login"),
   path("logout", views.logout_view, name="logout"),
   path("register", views.register, name="register"),
   path('coffee_admin',views.main_dashboard,name="main_dashboard"),
   path("coffee_admin/products",views.admin_products,name="admin_products"),
   path("get_product/<int:product_id>",views.get_product,name="get_product"),
   path('coffee_admin/users',views.admin_users,name='admin_users'),  
   path('home_products',views.home_products,name="products"),
   path('delete_product',views.delete_product,name="delete_product"),
   path('product_details/<int:product_id>',views.product_details,name="product_details"),
   path('save_product',views.save_product,name="save_product"),
   path('cart_items',views.cart_items,name="cart_items"),
   path('cart/<int:product_id>',views.add_to_cart,name="add_to_cart"),
   path('cart_items/<int:item_id>',views.cart_delete_item,name="cart_delete_item"),
   path('update_cart_item/<int:product_id>',views.update_cart_item,name="update_cart_item"),
   path('create_checkout_session/',views.create_checkout_session,name="create_checkout_session"),
   path('success_transaction/',views.success_transaction,name="success_transaction"),
   path('failure_transaction/',views.failure_transaction,name="failure_transaction"),
   path('profile/<int:user_id>',views.profile,name="profile"),
   path('likes/<int:product_id>', views.toggle_like, name="likes"),
   path('webhook/',views.stripe_webhook, name="stripe_webhook"),
   path('api/sales-data',views.sales_data,name="sales_data")
   
]