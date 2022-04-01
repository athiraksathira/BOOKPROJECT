from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from owner.models import Books


class Carts(models.Model):
    product=models.ForeignKey(Books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    options=(
        ("incart","incart"),
        ("orderplaced","orderplaced"),
        ("cancelled","cancelled")


    )
    status=models.CharField(max_length=120,choices=options,default="incart")
