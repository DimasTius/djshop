from django.db import models

# Create your models here.
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    color = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    gender = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Catalog', on_delete=models.PROTECT, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_id': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('title', )

class Catalog(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Каталог'
        ordering = ('name', )
