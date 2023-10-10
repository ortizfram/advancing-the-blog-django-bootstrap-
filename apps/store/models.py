from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sessions.models import Session  # Import the Session model

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                null=True, 
                                blank=True)
    name = models.CharField(max_length=200, 
                            null=True)
    email = models.CharField(max_length=200, 
                             null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    price = models.DecimalField(max_digits=7,decimal_places=2)
    name = models.CharField(max_length=200, 
                            null=True)
    digital = models.BooleanField(default=False,
                                  null=True, 
                                  blank=True)
    image = models.ImageField(null=True, 
                              blank=True, 
                              upload_to='products/')#subdirectory under MEDIA_ROOT

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try: 
            url = self.image.url
        except:
            url = ""
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    session_id = models.CharField(max_length=32, null=True, blank=True)  # Add this field for session ID
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"Order ID: {self.id}, Customer: {self.customer.name if self.customer else 'N/A'}"

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def save(self, *args, **kwargs):
        # Check if this order is complete before saving
        if self.complete:
            # Mark all other orders for this customer as complete
            if self.customer:
                Order.objects.filter(customer=self.customer, complete=False).exclude(id=self.id).update(complete=True)
        super(Order, self).save(*args, **kwargs)

    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    country = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    


