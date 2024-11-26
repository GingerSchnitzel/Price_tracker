from django.shortcuts import render
from django.contrib import messages
import requests
from bs4 import BeautifulSoup
from ..models import Product, ProductPrice, UserInterest
from ..forms import ProductLinkForm
from decimal import Decimal 
from django.contrib.auth.decorators import login_required


def scrape_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the product price in the <p> element with the class "product-new-price"
        #<p class="product-new-price" data-test="main-price">5.537<sup><small class="mf-decimal">,</small>58</sup> <span>Lei</span></p>
        price_element = soup.find('p', class_='product-new-price', attrs={'data-test': 'main-price'})

        #<h1 class="page-title" data-test="page-title"> Apple iPad Pro 11" (2024), 256GB, Wi-Fi, Standard glass, Space Black</h1>
        name_element = soup.find(class_='page-title')
        #print(name_element)
        #<img src="https://s13emagst.akamaized.net/products/71017/71016711/images/res_588aeec96433f53c1d361717c93f7ee1.jpg?width=720&amp;height=720&amp;hash=96C29E1E754347C0AC64BB4ACD77D87E" alt="Apple iPad Pro 11&quot; (2024), 256GB, Wi-Fi, Standard glass, Space Black" referrerpolicy="unsafe-url" data-test="main-product-gallery">

        image_element = soup.find('img', attrs={'data-test':'main-product-gallery'})

        if price_element is None or name_element is None or image_element is None:
            return None, None, None

        # Extract the main price part and the fractional part
        main_price = price_element.contents[0].strip()  # Main price, e.g., "5.537"
        fraction = price_element.find('sup').get_text().strip()  # Fractional part, e.g., "58"

        #print(main_price)
        #print(fraction)

        # Combine main price and fraction into a complete price
        full_price = f"{main_price}.{fraction}".replace('.', '').replace(',', '.')  # Handle Romanian decimal format
        #print(full_price)
        price_value = Decimal(full_price)

        name = name_element.get_text().strip()

        #removing everything after '?' so we get the link to the image
        final_image = image_element.get('src').split('?')[0]

        return price_value, name, final_image
     
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

@login_required       
def add_product(request):
    if request.method == 'POST':
        print("in post method")
        form = ProductLinkForm(request.POST)
        print(form.errors)

        if form.is_valid():
            print("form is valid")
            url = form.cleaned_data['url']
            print("Product url", url)
            product = Product.objects.filter(url=url)
            notify = form.cleaned_data['notify']

            if product.exists():
                print("found product", product[0].name)
                if UserInterest.objects.filter(user= request.user, product=product[0]).exists():
                    print("Product", product[0].name, "already exists in", request.user.username, "interests.")
                    messages.error(request, f"Product {product[0].name} already exists in your tracking list.")
                  
                else:
                    print("Adding product", product[0].name, "to", request.user.username +"'s tracking list.")
                    user_interest = UserInterest.objects.create(user=request.user, product=product[0], notify = notify)
                    messages.success(request, f"Product {product[0].name} has been successfully added to your tracking list.")
                return render(request, 'tracker.html', {'form': form})
            print("Did not find product in database, adding:", url)

            # Scrape price from the product page
            price, name, image = scrape_data(url)

            if price is None or name is None:
                messages.error(request, "Could not retrieve the price or name from the provided URL.")
                return render(request, 'tracker.html', {'form': form})

            product= Product.objects.create(url=url, name=name, image_url=image)
            product_price = ProductPrice.objects.create(product=product, price=price)
            user_interest = UserInterest.objects.create(user=request.user, product=product, notify = notify)

            # Notify the user that the product was successfully added
            messages.success(request, f"Product {name} has been added to the database with a price of {price} RON.")
            return render(request, 'tracker.html', {'form': form})
        else:
            print("Form is not valid.")
        
    else:
        form = ProductLinkForm()

    return render(request, 'tracker.html', {'form': form})