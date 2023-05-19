from django.urls import path
from .views import *

urlpatterns = [
    path('', head_page, name='home'),
    path('logout/', logout_view, name='logout'),
    path('profile/', register_and_login, name='profile'),
    path('cart/', cart, name='cart'),
    path('add_prod_cart/', add_prod_cart, name='add_prod_cart'),
    path('liked/', liked, name='like'),
    path('add_prod_liked/', add_prod_liked, name='add_prod_liked'),
    path('product/<slug:prod_slug>/', show_product, name='product'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<slug:cat_slug>/', show_cat, name='catalog_slug'),
    path('search/', search, name='search')
]
