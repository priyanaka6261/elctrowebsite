from django.contrib import admin
from .models import User,Product,Wishlist,Cart
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)

# Register your models here.
