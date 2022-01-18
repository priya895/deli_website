
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


#username, email, password, 
class User(AbstractUser):
    pass
class Category(models.Model):
    type=models.CharField(blank=True,max_length=200)
    def __str__(self):
        return f"{self.id} : {self.type}"
class Auctions(models.Model):
    Title=models.CharField(max_length=64)
    Description= models.CharField(max_length= 1000)
    ImageURL=models.ImageField(null=True,blank= True)
    Startingbid=models.IntegerField(null = True)
    Currentbid= models.IntegerField(null = True,blank=True)
    Creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name="auctions")
    Active=models.BooleanField(default=True)
    Category= models.ForeignKey(Category,on_delete= models.CASCADE,related_name="category", null=True)
    Win = models.ForeignKey(User,on_delete=models.CASCADE,related_name= "winner",null=True,blank=True)
    def __str__ (self):
        return f"{self.id} {self.Title} creator: { self.Creator}"

class Wishlist(models.Model):
    Watcher= models.ForeignKey(User,on_delete=models.CASCADE,related_name= "listings")
    Item = models.ManyToManyField(Auctions,blank=True,related_name="watcher_list")
    
    def __str__(self):
        return f"{ self.Watcher} : {self.Item}"
    
class Bid(models.Model):
    Item = models.ForeignKey(Auctions,on_delete=models.CASCADE,related_name= "item")
    price= models.IntegerField(null = True)
    Owner= models.ForeignKey(User,on_delete=models.CASCADE,related_name="bids",null=True)

class Comments(models.Model):
    watcher=models.ForeignKey(User,on_delete=models.CASCADE,related_name="User")
    comment= models.CharField(max_length= 1000, null=True)
    Item=models.ManyToManyField(Auctions,max_length=64)
    def __str__(self):
        return f"{self.watcher}: {self.comment}"