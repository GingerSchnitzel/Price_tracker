from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime

class Product(models.Model):
    url = models.URLField(unique=True)  # Store the product link (URL)
    name = models.CharField(max_length= 500)
    image_url = models.URLField(default='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg')

    def __str__(self):
        return f"Product: {self.url}, Name: {self.name}"

# Model to store product links and prices
class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store the product price
    timestamp = models.DateTimeField(auto_now=True)  # Timestamp when price was last checked
    

    def __str__(self):
        return f"Product: {self.product.name}, Price: {self.price} RON, Timestamp: {localtime(self.timestamp)}"

# Model to store which users are interested in which products
class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    notify = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user.username} is interested in {self.product.name}. Notify: {self.notify}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    
