from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Category)
admin.site.register(models.Auction_listings)
admin.site.register(models.Comments)
admin.site.register(models.Bids)
admin.site.register(models.Watch_list)


