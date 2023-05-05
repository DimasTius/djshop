from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.template import loader
from .models import *
from .forms import *

menu = (
        {'title': "profile", 'url_name': 'profile'},
        {'title': "like", 'url_name': 'like'},
        {'title': "cart", 'url_name': 'cart'},
        {'title': "sand", 'url_name': 'catalog'}
)

def head_page(request):
    prods = Product.objects.all()
    title = 'Главная страница'
    context = {'title': title, 'prods': prods, 'menu': menu}
    return render(request, 'product/head_page.html', context)

def catalog(request):
    cats = Catalog.objects.all()
    title = 'Каталог'
    context = {'title': title, 'menu': menu, 'cats': cats}
    return render(request, 'product/catalog.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def register_and_login(request):
    if request.user.is_authenticated:
        title = 'Профиль'
        context = {'title': title, 'menu': menu, 'logout': 'logout'}
        return render(request, 'product/profile.html', context=context)
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password1')
            user_exists = User.objects.filter(username=username).exists()
            if user_exists:
                # Если пользователь существует, то производим авторизацию
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
            elif form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
        else:
            form = UserCreationForm()
    title = 'Профиль'
    context = {'title': title, 'menu': menu, 'form': form}
    return render(request, 'product/form_prof.html', context=context)

def like(request):
    return HttpResponse('понравившиеся')

def cart(request):
    return HttpResponse('корзина')

def show_product(request, prod_slug):
    prod = get_object_or_404(Product, slug=prod_slug)
    #photos = Picture.objects.filter(pk=prod_id)

    context = {
        #'photos': photos,
        'prod': prod,
        'menu': menu,
        'title': prod.title,
    }

    return render(request, 'product/prod.html', context=context)

def show_cat(request, cat_slug):
    prods = Product.objects.filter(cat__slug=cat_slug)
    title = f'Каталог {cat_slug}'
    context = {'title': title, 'prods': prods, 'menu': menu}
    return render(request, 'product/head_page.html', context)

def pageNotFound(request, exception):
    return HttpResponseNotFound('вы бля дь куда зашли')

"""
template = loader.get_template('путь до шаблона')
context = {контекст}
return HttpResponse(template.render(context, request)) 
загрузить шаблон, заполнить контекст и вернуть объект HttpResponse с результатом визуализации шаблона
"""
