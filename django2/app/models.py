from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver 

# @receiver(post_save,sender=User)
# def AfterUserSave(sender,instance,created,**kwargs):
    # if created:

class Product(models.Model):
    name=models.CharField(max_length=10)
    title=models.CharField(max_length=100)
    price=models.IntegerField()
    
class Cart(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid4)
    created_at=models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items",default="")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default="")
    quantity=models.PositiveSmallIntegerField()
    
    
    class Meta:
        unique_together=[['cart','product']]
    


# /////////////////////////////////order models /////////////////////////////////////////////////


class Order(models.Model):
    placed_at=models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=1,default="p")
    customer=models.ForeignKey(User,on_delete=models.PROTECT)
    
    def __str__(self):
        return self.customer.username
    
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.PROTECT,related_name="items")
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name="orderitems")
    quantity=models.PositiveSmallIntegerField()
    
    
    def __str__(self):
        return self.product.name

