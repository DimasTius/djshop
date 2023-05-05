from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')
    color = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    gender = models.CharField(max_length=50)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Catalog', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('title', )

class Catalog(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog_slug', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Каталог'
        ordering = ('name', )

class Picture(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'
        ordering = ('product', )


