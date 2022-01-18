from django.urls import path

from . import views

urlpatterns = [
    path("", views.active, name="index"),
    path("all",views.all, name="all"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/<int:id>",views.show,name = "show"),
    path("create",views.create,name="create"),
    path("active",views.active,name="active"),
    path("wishlist/<int:id>",views.wishlist, name="wishlist"),
    path("showlist",views.showlist,name="showlist"),
    path("addcomment/<int:id>",views.addcomment,name="comment"),
    path("remove/<int:id>",views.remove,name= "remove"),
    path("auctions/placebid/<int:id>",views.placebid, name = "placebid"),
    path("category",views.category,name="category"),
    path("close/<int:id>",views.close,name="close")

]
