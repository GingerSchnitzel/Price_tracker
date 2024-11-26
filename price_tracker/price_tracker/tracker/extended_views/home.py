from django.shortcuts import render
from ..models import Product, ProductPrice, UserInterest
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == 'GET':
        user_products = UserInterest.objects.filter(user= request.user)
        products = []
        for product in user_products:
            name = product.product.name
            url = product.product.url
            image = product.product.image_url
            notify = 'checked' if product.notify else 'unchecked'
            #print(notify)
            price_obj = ProductPrice.objects.filter(product=product.product).order_by('-timestamp').first()
            price = price_obj.price if price_obj else "N/A" #Handles the case when price is none
            products.append({
                "name": truncate_text(name,80),
                "price": price, #instead of price.price
                "url": url,
                "image": image, 
                "notify": notify,
                })
            
        return render(request, 'home.html', {'products':products})    

def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text
