from django.shortcuts import redirect
from ..models import Product, ProductPrice, UserInterest
from django.contrib.auth.decorators import login_required


@login_required
def toggle_notify(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        product = Product.objects.filter(url= url).first()
        user_interest = UserInterest.objects.filter(user=request.user, product=product).first()
        user_interest.notify = not user_interest.notify
        user_interest.save()
    return redirect ('home')

@login_required
def delete_product(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        product = Product.objects.filter(url= url).first()
        user_interest = UserInterest.objects.filter(user=request.user, product=product).first()
        user_interest.delete()
    return redirect ('home')
    
