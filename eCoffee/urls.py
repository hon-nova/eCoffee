from django.urls import path,include

from . import views
urlpatterns =[
   path('',views.index,name="index"),
   path("login", views.login_view, name="login"),
   path("logout", views.logout_view, name="logout"),
   path("register", views.register, name="register"),
   path("coffee_admin/dashboard",views.admin_dashboard,name="admin_dashboard"),
   path('products',views.products,name="products"),
   path('coffee_admin/users',views.users,name='users'),
   path('admin_products',views.admin_products,name="admin_products"),
   path('create_product',views.create_product,name="create_product"),
]