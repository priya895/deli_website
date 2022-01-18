
from django.contrib import admin
from .models import *

admin.site.register(Auctions)
admin.site.register(Wishlist)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comments)
admin.site.register(Category)

