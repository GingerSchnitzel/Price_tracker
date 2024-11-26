from django.contrib import admin
from .models import Product, ProductPrice, UserInterest, ContactMessage

# Register your models
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(UserInterest)
admin.site.register(ContactMessage)