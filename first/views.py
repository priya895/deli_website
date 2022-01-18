from django.shortcuts import redirect,render
from django.http.response import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required

from django.urls import *
from . models import *

def layout(request):
    c=Categories.objects.all()
    return (request, "first/layout.html",{
        "cat":c,
    })
# Create your views here.
# @login_required(login_url='/login')
def index(request):
    product =Products.objects.all()
    # c=Categories.objects.all()
    return render(request,"first/index.html",{
        "p":product,    
    })
def post(request):
     if request.method=="POST":
         pro=Products()
         pro.Title=request.POST["Title"]
         pro.Description=request.POST["Description"]
         pro.Image=request.POST["Image"]
         pro.price=request.POST["price"]
         pro.save()
         return HttpResponseRedirect (reverse("index"))
     else:
         return render(request, "first/form.html")
def about(request):
    return render(request,"first/about.html")
def contact(request):
    return render(request, "first/contact.html")
def home(request):
    return render(request,"first/index.html")
def addcomment(request,id):
    cUser=request.user
    product=Products.objects.get(id=id)
    if request.method == "POST":
        c=Comments.objects.create(user=cUser)
        c.Items=product
        c.comment=request.POST["comment"]
        c.save()
        return HttpResponseRedirect(reverse("fshow",args=[id]))
    else:
        return render(request,"first/comment.html",{
            "id":product.id
        })
def fshow(request,id):
    p=Products.objects.get(id=id)
    comments= Comments.objects.filter(Items=p).all()
    return render (request,"first/fshow.html",{
        "id": id,
        "product": p,
       "comments":comments,
    }) 
@login_required(login_url='/login')
def fwishlist(request):
    current=request.user
    try:
        instance= Wishlist.objects.get(user=current)
        return render(request, "first/index.html",{
            "p":instance.item.all(),
            "wishlist": True,
        })
    except Wishlist.DoesNotExist:
        return HttpResponse("NO items in your Wishlist")
def categories(request,id):
    c=Categories.objects.get(id=id)
    p=Products.objects.filter(category=c)
    return render(request,"first/index.html",{
          "p":p,

    })
def categories(request):
    if request.method=='POST':
        c= request.POST["category"]
        return render(request, "first/index.html",{
            "p":Products.objects.filter(category=c)
         })
    else :
        return render(request,"first/categories.html",{
           "p":Categories.objects.all()
        })
@login_required(login_url='/login')
def addwish(request,id):
    current=request.user
    try:
        w=Wishlist.objects.get(user=current)
    except Wishlist.DoesNotExist:
        w=Wishlist.objects.create(user=current)
    p=Products.objects.get(id=id)
    w.item.add(p)
    w.save()
    return redirect("fwishlist")
@login_required(login_url='/login')
def remwish(request,id):
    current=request.user
    try:
        w=Wishlist.objects.get(user=current)
    except:
        return HttpResponseRedirect("you have no wishlist yet!!")
    p=Products.objects.get(id=id)
    w.item.remove(p)
    w.save()
    return redirect("fwishlist")
@login_required(login_url='/login')
def fcart(request):
    current=request.user
    try:
        instance= Cart.objects.get(user=current)
        return render(request, "first/index.html",{
            "p":instance.items.all(),
            "cart":True,
        })
    except Cart.DoesNotExist:
        return HttpResponse("NO items in your cart")
@login_required(login_url='/login')
def addcart(request,id):
    current=request.user
    try:
        w=Cart.objects.get(user=current)
    except Cart.DoesNotExist:
        w=Cart.objects.create(user=current)
    p=Products.objects.get(id=id)
    w.items.add(p)
    w.save()
    return redirect("fcart")
@login_required(login_url='/login')
def remcart(request,id):
    current=request.user
    try:
        w=Cart.objects.get(user=current)
    except:
        return HttpResponse("you have not added items to your cart yet!!")
    p=Products.objects.get(id=id)
    w.items.remove(p)
    w.save()
    return redirect("fcart")
  