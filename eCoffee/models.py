from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models


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
    
class CartItem(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="user_products")
    amount_paid=models.DecimalField(decimal_places=2,max_digits=10)