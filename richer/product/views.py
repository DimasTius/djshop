from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from django.template import loader
from .models import Product

menu = ('о сайте', 'поиск', 'профиль', 'понравившиеся', 'корзина')

def head_page(request):
    template = loader.get_template('product/head_page.html')
    data = '<h1>Список предлагаемых продуктов от richer</h1>'
    title = 'Главная страница'
    context = {'title': title, 'data': data, 'menu': menu}
    return HttpResponse(template.render(context, request))

def categories(request):
    prods = Product.objects.all()
    title = 'Категории'
    context = {'title': title, 'menu': menu, 'prods': prods}
    return render(request, 'product/category.html', context)

def test(request):
    print(request.GET)
    return HttpResponse('test')

def pageNotFound(request, exception):
    return HttpResponseNotFound('вы бля дь куда зашли')
