from django.urls import path,include

from . import views
urlpatterns =[
   path('',views.index,name="index"),
   path("login", views.login_view, name="login"),
   path("logout", views.logout_view, name="logout"),
   path("register", views.register, name="register"),
   path("coffee_admin/dashboard",views.admin_dashboard,name="admin_dashboard"),
   path('products',views.products,name="products")
]