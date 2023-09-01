# Подключение библиотек
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.template import loader
from .models import *
from .forms import *

# Вывод меню на главной странице сайта
menu = (
        {'title': "profile", 'url_name': 'profile'},
        {'title': "like", 'url_name': 'like'},
        {'title': "cart", 'url_name': 'cart'},
        {'title': "sand", 'url_name': 'catalog'}
)

# Контроллер главной страницы
def head_page(request):
    prods = Product.objects.all()
    title = 'Главная страница'
    context = {'title': title, 'prods': prods, 'menu': menu}
    return render(request, 'product/head_page.html', context)

# Контроллер каталога
def catalog(request):
    cats = Catalog.objects.all()
    title = 'Каталог'
    context = {'title': title, 'menu': menu, 'cats': cats}
    return render(request, 'product/catalog.html', context)

# Контроллер поиска
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

# Функция отображения выхода
def logout_view(request):
    logout(request)
    return redirect('profile')

# Функция регистрации и входа
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
        title = 'Авторизация'
        context = {'title': title, 'menu': menu}
        return render(request, 'product/form_prof.html', context=context)



# Регистрация пользователя
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserRegistrationForm()

    title = 'Регистрация'
    context = {'title': title, 'menu': menu, 'form': form}
    return render(request, 'product/register.html', context=context)

# Вход пользователя
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
                # Дополнительная обработка или перенаправление на другую страницу
    else:
        form = UserLoginForm()
    title = 'Вход'
    context = {'title': title, 'menu': menu, 'form': form}
    return render(request, 'product/login.html', context=context)

# Функция отображение избранного
def liked(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(likedproduct__user=request.user)
        title = 'Избранное'
        context = {'title': title, 'menu': menu, 'products': products}
        return render(request, 'product/liked.html', context=context)
    else:
        return redirect('profile')

# Добавить товар в избранное
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

# Контроллер корзины
def cart(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(cartproduct__user=request.user)
        total_amount = products.aggregate(amount=Sum('price'))['amount']
        title = 'Корзина'
        context = {'title': title, 'menu': menu, 'products': products, 'is_cart': 'Удалить из корзины', 'amount': total_amount}
        return render(request, 'product/cart.html', context=context)
    else:
        return redirect('profile')

# Добавить продукт в корзину
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

# Удалить из корзины продукт
def remove_prod_cart(request):
    if request.user.is_authenticated:
        prod_id = request.POST.get('prod_id')
        user = request.user
        cart_products = get_object_or_404(CartProduct, user=user)
        product = get_object_or_404(Product, id=prod_id)
        cart_products.cart.remove(product)
        return redirect('cart')
    else:
        return redirect('profile')

# Уникальная страница продукта
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

def delivery(request):
    pass

# Страница с категориями
def show_cat(request, cat_slug):
    prods = Product.objects.filter(cat__slug=cat_slug)
    title = f'Каталог {cat_slug}'
    context = {'title': title, 'prods': prods, 'menu': menu}
    return render(request, 'product/head_page.html', context)

# Обработка ошибки не найденной страницы
def pageNotFound(request, exception):
    return HttpResponseNotFound('Страница не найдена')

"""
template = loader.get_template('путь до шаблона')
context = {контекст}
return HttpResponse(template.render(context, request)) 
загрузить шаблон, заполнить контекст и вернуть объект HttpResponse с результатом визуализации шаблона
"""
