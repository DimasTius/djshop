from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    content = models.TextField(blank=True)
    gender = models.CharField(max_length=50)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    is_published = models.BooleanField(default=True)