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

def search(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(search_names__icontains=query)

        context = {
            'query': query,
            'products': products,
            'menu': menu
        }
        return render(request, 'product/search_results.html', context)
    else:
        return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('profile')

def register_and_login(request):
    user = request.user
    if request.user.is_authenticated:
        title = 'Профиль'

        if request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                form.save(user)

        context = {'title': title,
                   'menu': menu,
                   'logout': 'logout',
                   'user': user,
                   }
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
            elif form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                form.save()
                user = authenticate(username=username, password=password)
                login(request, user)
            return redirect('profile')
        else:
            form = UserCreationForm()
    title = 'Профиль'
    context = {'title': title, 'menu': menu, 'form': form}
    return render(request, 'product/form_prof.html', context=context)

def liked(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(likedproduct__user=request.user)
        title = 'Избранное'
        context = {'title': title, 'menu': menu, 'products': products}
        return render(request, 'product/liked.html', context=context)
    else:
        return redirect('profile')

def add_prod_liked(request):
    if request.user.is_authenticated:
        prod_id = request.POST.get('prod_id')  # id продукта, который нужно добавить в избранное
        user = request.user  # текущий пользователь

        # получаем экземпляр модели LikedProduct для текущего пользователя
        liked_products, created = LikedProduct.objects.get_or_create(user=user)

        # получаем экземпляр модели Product, который нужно добавить в список избранного
        product = get_object_or_404(Product, id=prod_id)
        if product in liked_products.liked.all():
            liked_products.liked.remove(product)
        else:
            # добавляем продукт в список избранного пользователя
            liked_products.liked.add(product)

        return redirect('product', prod_slug=product.slug)
    else:
        return redirect('profile')

def cart(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(cartproduct__user=request.user)
        title = 'Корзина'
        context = {'title': title, 'menu': menu, 'products': products}
        return render(request, 'product/cart.html', context=context)
    else:
        return redirect('profile')

def add_prod_cart(request):
    if request.user.is_authenticated:
        prod_id = request.POST.get('prod_id')  # id продукта, который нужно добавить в избранное
        user = request.user  # текущий пользователь

        # получаем экземпляр модели LikedProduct для текущего пользователя
        cart_products, created = CartProduct.objects.get_or_create(user=user)

        # получаем экземпляр модели Product, который нужно добавить в список избранного
        product = get_object_or_404(Product, id=prod_id)
        if product in cart_products.cart.all():
            cart_products.cart.remove(product)
        else:
            # добавляем продукт в список избранного пользователя
            cart_products.cart.add(product)

        return redirect('product', prod_slug=product.slug)
    return redirect('profile')

def show_product(request, prod_slug):
    if request.user.is_authenticated:
        liked_products, created = LikedProduct.objects.get_or_create(user=request.user)
        cart_products, created = CartProduct.objects.get_or_create(user=request.user)
        prod = get_object_or_404(Product, slug=prod_slug)
        if prod in liked_products.liked.all():
            is_liked = 'Удалить из избранного'
        else:
            is_liked = 'Добавить в избранное'
        if prod in cart_products.cart.all():
            is_cart = 'Удалить из корзины'
        else:
            is_cart = 'Добавить в корзину'

        #photos = Picture.objects.filter(pk=prod_id)

        context = {
            #'photos': photos,
            'prod': prod,
            'menu': menu,
            'title': prod.title,
            'is_liked': is_liked,
            'is_cart': is_cart,
            'log': True
        }
    else:
        prod = get_object_or_404(Product, slug=prod_slug)
        context = {
            # 'photos': photos,
            'prod': prod,
            'menu': menu,
            'title': prod.title,
            'log': False
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
