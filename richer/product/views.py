from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from django.template import loader
from .models import Product

menu = (
        {'title': "profile", 'url_name': 'profile'},
        {'title': "like", 'url_name': 'like'},
        {'title': "cart", 'url_name': 'cart'},
        {'title': "sand", 'url_name': 'sand'}
)

def head_page(request):
    prods = Product.objects.all()
    title = 'Главная страница'
    context = {'title': title, 'prods': prods, 'menu': menu}
    return render(request, 'product/head_page.html', context)

def catalog(request):
    title = 'Каталог'
    context = {'title': title, 'menu': menu, 'data': '<h1>Список каталога</h1>'}
    return render(request, 'product/catalog.html', context)

def profile(request):
    return HttpResponse('профиль')

def like(request):
    return HttpResponse('понравившиеся')

def cart(request):
    return HttpResponse('корзина')

def show_product(request, prod_id):
    return HttpResponse(f"Отображение продукта с id = {prod_id}")

def pageNotFound(request, exception):
    return HttpResponseNotFound('вы бля дь куда зашли')

"""
template = loader.get_template('путь до шаблона')
context = {контекст}
return HttpResponse(template.render(context, request)) 
загрузить шаблон, заполнить контекст и вернуть объект HttpResponse с результатом визуализации шаблона
"""
