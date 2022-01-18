from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import comments
from django.shortcuts import get_list_or_404

from .models import *


def all(request):
        return render (request, "auctions/index.html",{
        "auctions": Auctions.objects.all(),
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request,"auctions/index.html",{
            "auctions": Auctions.objects.all(),
        })
    else:
        return render(request, "auctions/register.html")
def show (request,id):
    auction=Auctions.objects.get(id=id)
    comments= Comments.objects.filter(Item=auction).all()
    return render (request,"auctions/show.html",{
        "id": id,
        "auction": auction,
       "comments":comments,
    }) 
@login_required(login_url='/login')  
def wishlist(request,id):
    current=request.user
    auction=Auctions.objects.get(id=id)
    try:
        instance= Wishlist.objects.get(Watcher=current)
    except Wishlist.DoesNotExist:
        instance=Wishlist.objects.create(Watcher=current)
    instance.Item.add(auction)
    instance.save()
    return HttpResponseRedirect(reverse("showlist"))
  
def showlist(request):
    current=request.user
    try:
        c=Wishlist.objects.get(Watcher=current)
        return render (request, "auctions/index.html",{
            "auctions": c.Item.all(),
            "wishlist":True
        })
    except Wishlist.DoesNotExist:
        return HttpResponse("you have nothing to show in your wishlist")
def remove(request,id):
    current = request.user
    b= Wishlist.objects.get(Watcher=current)
    c= Auctions.objects.get(id=id)
    b.Item.remove(c)
    return render (request, "auctions/index.html",{
        "auctions": b.Item.all(),
        "wishlist":True
    })

@login_required(login_url='/login')  
def create (request):
    if request.method =='POST': 
        current=request.user
        auc= Auctions()
        auc.Title= request.POST["Title"]
        auc.Description=request.POST["Description"]
        auc.ImageURL= request.POST["ImageURL"]
        auc.Startingbid= request.POST["Startingbid"]
        aucc=request.POST["category"]
        auc.Category=Category.objects.get(id=aucc)
        auc.Creator=User.objects.get(id=current.id)
        auc.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new.html",{
            "list":Category.objects.all()
        })    
#addcomment/<int:id>   views.addcomment
@login_required(login_url='/login')
def addcomment(request,id):
    current= request.user
    auction= Auctions.objects.get(id=id)
    if request.method =='POST':
        c= Comments.objects.create(watcher=current)
        c.Item.add(auction)
        c.comment=request.POST["comment"]
        c.save()
        return redirect('show',id=id)
    else: 
        return render(request,"auctions/addcomment.html",{
            "id":auction.id
        })

def active(request):
    auction =Auctions.objects.filter(Active=True)
    return render (request, "auctions/index.html",{
        "auctions": auction,
    })
@login_required(login_url='/login')
def placebid (request,id):
    if request.method == "POST":
        current=request.user
        auc= Auctions.objects.get(id=id)
        try:
            bid=Bid.objects.get(Owner=current,Item=auc)
        
        except Bid.DoesNotExist:
            bid =Bid.objects.create(Owner=current,Item=auc)
            bid.save()
        c=request.POST["bid"]
        d=int(c)
        if auc.Currentbid is None:
            if d > auc.Startingbid:
                Auctions.objects.filter(id=id).update(Currentbid=c)
                Bid.objects.filter(Owner=current,Item=auc).update(price=c)
            else:
                return render(request, "auctions/placebid.html",{
                    "message": "value must be greater than current bid",
                    "id":id
                })
                
        elif d > auc.Currentbid and d > auc.Startingbid:
            Auctions.objects.filter(id=id).update(Currentbid=c)
            Bid.objects.filter(Owner=current,Item=auc).update(price=c)
   
        else:
            return render(request, "auctions/placebid.html",{
                "message": "value must be greater than current bid",
                "id":id
            })
        auction=Auctions.objects.get(id=id)
        comments= Comments.objects.filter(Item=auction).all()
        return render(request,"auctions/show.html",{
            "message": "Bid is placed",
            "auction": auction,
            "id":id,
            "comments":comments
        })
            
    else:
        return render (request, "auctions/placebid.html",{
            "id": id
        })
def category(request):
    if request.method=='POST':
        auc= request.POST["category"]
        return render(request, "auctions/index.html",{
            "auctions":Auctions.objects.filter(Category=auc).all()
         })
    else :
        return render(request,"auctions/category.html",{
           "list":Category.objects.all()
        })
def close(request,id):
    auc= Auctions.objects.get(id=id)
    c= auc.Currentbid
    try :
        bid=Bid.objects.filter(Item=auc)
        bid1=bid.get(price=c)
        auc.Active=False
        auc.Win=bid1.Owner
        auc.save()
        return redirect ('show',id=id)
    except Bid.DoesNotExist:
        return HttpResponse("NO bids placed on this listing")
        
    

