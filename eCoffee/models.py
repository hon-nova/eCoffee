from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from django.utils import timezone

class User(AbstractUser):
    pass 

class Product(models.Model):
    CATEGORY_CHOICES=[
        ("JAVA WORKS","JAVA WORKS"),
        ("NESCAFE","NESCAFE"),
        ("TIM HORTONS","TIM HORTONS"),
        ("ETHICAL BEAN","ETHICAL BEAN"),
        ("MAXWELL HOUSE","MAXWELL HOUSE"),
        ("FOLGERS","FOLGERS"),
        ("STARBUCK","STARBUCK"),
        ("NABOB","NABOB"),
        ("LAVAZZA","LAVAZZA"),
        ("49TH PARALLEL","49TH PARALLEL"),
        ("KICKING HORSE","KICKING HORSE"),
        ("LIFEBOOST","LIFEBOOST"),
        ("VAN HOUTTE","VAN HOUTTE")
    ]    
    description=models.TextField()
    category=models.CharField(max_length=14,choices=CATEGORY_CHOICES)   
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity=models.IntegerField()
    photo_url=models.URLField()
    created_at=models.DateTimeField(auto_now_add=True)   
    
    def __str__(self):
        return f'product_id: {self.id} {self.description}, price ${self.price}'
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_likes")    

    class Meta:
        unique_together = ['user', 'product'] 
        
    def __str__(self):
        return f'{self.user.username} likes this coffee brand {self.product.description}'
     
class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE) 
    
    def __str__(self):
        return f'this cart {self.id} is for username: {self.user.username}'
    
    def get_total_items(self):
        return sum(item.quantity_purchased for item in self.cart_items.all())
    
    def get_total_price(self):
    
        return int(100*Decimal(1.12) * sum(Decimal(item.product.price)*item.quantity_purchased for item in self.cart_items.all()))  
    
class CartItem(models.Model):

    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items")
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity_purchased=models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'item: {self.product.description} with quantity: {self.quantity_purchased}'   
    
class Order(models.Model):

    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)   
    payment_status=models.BooleanField(default=False)
    
    placed_order_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    amount=models.FloatField(default=0)  
    
    def get_total_payment(self):
        return self.cart.get_total_price()
    
    def __str__(self):
        return f'Order id {self.id} for {self.cart.user.username} with status {"successful" if self.payment_status else "canceled"} with amount received CAD$ {self.amount}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='purchased_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_purchased = models.PositiveIntegerField(default=0)
    sub_total = models.FloatField(default=0)

    def __str__(self):
        return f'{self.product} - Quantity: {self.quantity_purchased}'

    def save(self, *args, **kwargs):
        self.sub_total = self.product.price * self.quantity_purchased
        super().save(*args, **kwargs)
 
    

        
    
 



    

        
    
    