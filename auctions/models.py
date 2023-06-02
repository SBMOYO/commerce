from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_listings(models.Model):
    item_name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.TextField(max_length=500)
    image = models.ImageField(null=True, blank=True, upload_to='images/', default='default.jpg')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=True)
    listed_by = models.ForeignKey("User", on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    

    def __str__(self):
        return self.item_name



class Bids(models.Model):
    item = models.ForeignKey("Auction_listings", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)

    def __int__(self):
        return self.item


class Comments(models.Model):
    item = models.ForeignKey("Auction_listings", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return self.comment



class Watch_list(models.Model):
    item = models.ForeignKey("Auction_listings", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return self.item


class Category(models.Model):
    Category = models.CharField(max_length=64)

    def __str__(self):
        return self.Category

