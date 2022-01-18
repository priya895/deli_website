from django.contrib.auth.models import AbstractUser
from django.db import models
from auctions.models import *
from django.core.validators import URLValidator
# Create your models here.
# class EUser(AbstractUser):
#     pass
class Categories(models.Model):
    type=models.CharField(blank=True,max_length=200)
    def __str__(self):
        return f"{self.id} : {self.type}"
class Products(models.Model):
    Image=models.ImageField(null=True,blank =True)
    Title=models.CharField(max_length=64)
    Description=models.CharField(max_length=50)
    price=models.IntegerField(default=None)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,related_name="categories",null=True)
    
    def __str__(self):
        return f"{self.id}:{self.Title}"

class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="wishlist")
    item=models.ManyToManyField(Products,blank=True,related_name="item")
    cart=models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user}:{self.item}"

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="cart")
    items=models.ManyToManyField(Products,null=True,related_name="items")

    def __str__(self):
        return f"{self.user}:{self.items}"
    
class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="addComment")
    Items=models.ForeignKey(Products,on_delete=models.CASCADE,related_name="Items",null=True)
    comment=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.user} commented {self.comment} for product {self.Items}"


