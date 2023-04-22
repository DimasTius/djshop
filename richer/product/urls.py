from django.urls import path
from .views import *

urlpatterns = [
    path('', head_page, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('profile/', profile, name='profile'),
    path('cart/', cart, name='cart'),
    path('like/', like, name='like'),
    path('sand/', catalog, name='sand'),
    path('product/<int:prod_id>/', show_product, name='product')
]
