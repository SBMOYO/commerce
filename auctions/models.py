from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_listings(models.Model):
    item_name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.TextField(max_length=500)
    image = models.ImageField(upload_to='auction_listings/', default='default.jpg')
    category = models.ForeignKey("Category", on_delete=models.CASCADE)



class Bids(models.Model):
    item = models.ForeignKey("Auction_listings", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)


class Comments(models.Model):
    item = models.ForeignKey("Auction_listings", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)



class Watch_list(models.Model):
    item = models.ForeignKey("Auction_listings", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)


class Category(models.Model):
    Category = models.CharField(max_length=64)

