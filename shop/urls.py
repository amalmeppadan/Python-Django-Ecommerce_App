from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('login/',views.login_page,name="login"),
    path('cart/',views.cart_page,name="cart"),
    path ('fav',views.fav_page,name="fav"),
    path ('delete_fav/<str:fid>',views.delete_fav,name="delete_fav"),
    path ('favviewpage',views.favviewpage,name="favviewpage"),
    path('logout/',views.logout_page,name="logout"),
    path('delete_cart/<str:cid>',views.delete_cart,name="delete_cart"),
    path('collections/',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collectionsview"),
    path('collections/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    
]