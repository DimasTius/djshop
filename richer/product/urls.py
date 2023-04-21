from django.urls import path
from .views import *

urlpatterns = [
    path('', head_page),
    path('cats/', categories),
    path('test/', test)
]
