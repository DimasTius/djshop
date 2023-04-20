from django.urls import path
from .views import *

urlpatterns = [
    path('', head_page),
    path('cat/', categories)
]
