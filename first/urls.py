from django.urls import path

from . import views
urlpatterns =[
      path("", views.index, name="index"),
      path("post", views.post, name="post"),
      path("about", views.about,name="about"),
      path("contact", views.contact,name="contact"),
      path("fwishlist",views.fwishlist,name="fwishlist"),
      path("addwish/<int:id>",views.addwish,name="addwish"),
      path("removewish/<int:id>",views.remwish,name="removewish"),
      path("fcart",views.fcart,name="fcart"),
      path("addcart/<int:id>",views.addcart,name="addcart"),
      path("removecart/<int:id>",views.remcart,name="removecart"),
      path("comment/<int:id>",views.addcomment,name="comment"),
      path("fshow/<int:id>", views.fshow,name="fshow"),
      path("categories", views.categories,name="categories"),
]