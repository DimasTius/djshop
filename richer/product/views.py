from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
def head_page(request):
    return HttpResponse('<h1>Главная страница</h1>')

def categories(request, sl):
    return HttpResponse(f'<h1>Категории<h1><p>{sl}</p>')

def test(request):
    print(request.GET)
    return HttpResponse('test')

def pageNotFound(request, exception):
    return HttpResponseNotFound('вы бля дь куда зашли')
