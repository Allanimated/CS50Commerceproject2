from django.contrib import admin
from .models import AuctionListing,Comment, Watchlist, Bids, Category
# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bids)
admin.site.register(Category)

