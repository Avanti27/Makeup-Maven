from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Products(models.Model):
    CAT = (
        (1, "Foundation"),
        (2, "Concealer"),
        (3, "Compact"),
        (4, "Eye Shadow"),
        (5, "Lipstick"),
        (6, "Highlighter"),
        (7,"Eye Kajal"),
        (8,"Eyeliner"),
    )
    
    price = models.FloatField()
    category = models.IntegerField(choices=CAT)
    is_active = models.BooleanField(default=True, verbose_name="available")
    pimage = models.ImageField(upload_to="image")
     
     
  
    def __float__(self):
        return self.price


class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")
    pid = models.ForeignKey(Products, on_delete=models.CASCADE, db_column="pid")
    qty = models.IntegerField(default=1)

class Order(models.Model):
    order_id = models.CharField(max_length=50)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column="uid")
    pid = models.ForeignKey(Products, on_delete=models.CASCADE, db_column="pid")
    qty = models.IntegerField(default=1)
