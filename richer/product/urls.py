from django.urls import path
from .views import *

urlpatterns = [
    path('', head_page, name='home'),
    path('profile/', profile, name='profile'),
    path('cart/', cart, name='cart'),
    path('like/', like, name='like'),
    path('product/<int:prod_id>/', show_product, name='product'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<int:cat_id>/', show_cat, name='catalog'),
]
