from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def head_page(request):
    return HttpResponse('<h1>Главная страница</h1>')

def categories(request):
    return HttpResponse('<h1>Категории<h1>')