from django.urls import path,include

from . import views
urlpatterns =[
   path('',views.index,name="index"),
   path("login", views.login_view, name="login"),
   path("logout", views.logout_view, name="logout"),
   path("register", views.register, name="register"),
   path('coffee_admin',views.main_dashboard,name="main_dashboard"),
   path("coffee_admin/products",views.admin_products,name="admin_products"),
   path('coffee_admin/users',views.admin_users,name='admin_users'),  
   path('home_products',views.home_products,name="products"),
   path('create_product',views.create_product,name="create_product"),
]