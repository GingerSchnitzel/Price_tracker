from django.shortcuts import render
from ..models import Product, ProductPrice
from .add_product import scrape_data
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend
import matplotlib.pyplot as plt
import io
import base64
from django.utils.timezone import now, localtime
from django.contrib.auth.decorators import login_required
import numpy as np



def generate_price_graph(url):
    """Generates a price fluctuation graph for a product."""
    product = Product.objects.get(url=url)
    price_history = list(ProductPrice.objects.filter(product=product).order_by('timestamp'))
    if len(price_history) == 1:
        price, name, image = scrape_data(url)
        print(f"Only found one price entry. Latest price is {price}")
        if price is not None:
            new_product_price = ProductPrice(product=product, price=price, timestamp=now())
            price_history.append(new_product_price)
  
   # Extract price and timestamp
    prices = [entry.price for entry in price_history]
    timestamps = [localtime(entry.timestamp).strftime('%Y-%m-%d %H:%M') for entry in price_history]
    # Create the graph
    fig, ax = plt.subplots(figsize=(8, 4))  # Adjusted figure size

        # Create the bars
    bars = ax.bar(
        np.arange(len(timestamps)),  # X positions for each bar
        prices,  # Heights of the bars (prices)
        color='orange', 
        width=0.1
    )
    ax.set_xticks(np.arange(len(timestamps)))  # Ensure the ticks align with bar positions
    ax.set_xticklabels(timestamps, rotation=45, fontsize=8)  # Use timestamps as labels

    # Axis formatting
    ax.set_xlabel("Time", fontsize=10)  # Reduce the x-axis label font size
    ax.set_ylabel("Price (RON)", fontsize=10)  # Reduce the y-axis label font size
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels
    ax.tick_params(axis='x', labelsize=8)  # Reduce tick label size on x-axis
    ax.tick_params(axis='y', labelsize=8)  # Reduce tick label size on y-axis

    # Axis visibility settings
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.xaxis.set_tick_params(bottom=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)
   
   # Add text annotations on top of bars
    bar_color = bars[0].get_facecolor()  # Get the color of the bars

    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # X position of the text (center of the bar)
            bar.get_height() + 1,  # Y position of the text (on top of the bar)
            f"{round(bar.get_height(), 1)} RON", # The height value to display (price)
            horizontalalignment='center',
            color=bar_color,
            weight='bold',
            fontsize=8  # Adjust font size for the text
        )

    # Adjust layout to ensure everything fits nicely
    fig.tight_layout()


    # Save the graph to a BytesIO stream
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    graph = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return graph

@login_required
def product_price_graph(request):
    """Renders the product price graph in a template."""
    if request.method == 'POST':
        print("in POST of product_price_graph")
        url = request.POST.get('url')
        print(url)
        if not url:
            # If no URL is provided in POST
            return render(request, 'price_graph.html', {'error_message': "No product has been selected. Please select a product to show the price graph."})
        
        try:
            product = Product.objects.get(url=url)
            graph = generate_price_graph(url)
            return render(request, 'price_graph.html', {'graph': graph, 'product': product})
        except Product.DoesNotExist:
            # If the product doesn't exist in the database
            return render(request, 'price_graph.html', {'error_message': "The selected product does not exist."})
    else:
        print("not in POST")
        # Handle GET requests
        return render(request, 'price_graph.html', {'error_message': "No product has been selected. Please select a product to show the price graph."})